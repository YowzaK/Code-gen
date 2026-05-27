import json
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from pydantic import ValidationError
from app.core.logger import logger
from app.core.database import get_session
from app.repository.pipeline_repository import PipelineRepository
from app.services.planner_service import PlannerService
from app.models.pipeline_plan import PipelinePlan
from app.models.pipeline_state_db import PipelineStage, PipelineStatus
from openai import RateLimitError
from app.services.audit_service import AuditService
from app.core.event_types import PLAN_GENERATED, PLAN_APPROVED, CODE_GENERATED, CODE_SAVED, TESTS_GENERATED, QUALITY_CHECK_RUN, QUALITY_CHECK_FAILED
from app.services.codegen_service import CodegenService
from app.services.path_policy_service import PathPolicyService
from app.models.generated_code import CodeGenerationResult
from app.services.testgen_service import TestgenService
from app.models.generated_tests import TestGenerationResult
from app.services.quality_check_service import QualityCheckService

router = APIRouter()


@router.get("/")
async def get_all_pipelines(
    session: Session = Depends(get_session)
):
    pipelines = PipelineRepository.list_all(session)

    if not pipelines:
        raise HTTPException(
            status_code=404,
            detail="No development pipelines created"
        )

    return pipelines


@router.get("/{pipeline_id}")
async def get_pipeline_by_id(
    pipeline_id: str,
    session: Session = Depends(get_session)
):

    pipeline_state = PipelineRepository.get_by_id(session, pipeline_id)

    if pipeline_state is None:
        raise HTTPException(
            status_code=404,
            detail="Pipeline not found"
        )

    return pipeline_state


@router.post("/{pipeline_id}/plan")
async def generate_pipeline_plan(
    pipeline_id: str,
    session: Session = Depends(get_session)
):
    pipeline_state = PipelineRepository.get_by_id(session, pipeline_id)

    if pipeline_state is None:
        raise HTTPException(
            status_code=404,
            detail="Pipeline not found"
        )

    if pipeline_state.spec is None:
        raise HTTPException(
            status_code=400,
            detail="Pipeline does not contain a valid specification"
        )

    if pipeline_state.current_stage != PipelineStage.VALID.value:
        raise HTTPException(
            status_code=400,
            detail=f"Planning cannot start from current stage: {pipeline_state.current_stage}"
        )

    try:

        generated_plan = await PlannerService.generate_plan(
            pipeline_state.spec
        )

        validated_plan = PipelinePlan(**generated_plan)

        pipeline_state.plan = validated_plan.model_dump()
        pipeline_state.current_stage = PipelineStage.PLANNED.value
        pipeline_state.status = PipelineStatus.PLANNED.value


        updated_pipeline = PipelineRepository.update(
            session=session,
            pipeline_state=pipeline_state
        )


        AuditService.log_event(
            session=session,
            pipeline_id=updated_pipeline.pipeline_id,
            event_type=PLAN_GENERATED,
            event_message="Implementation plan generated successfully",
            event_payload={
                "current_stage": updated_pipeline.current_stage,
                "status": updated_pipeline.status,
                "plan": updated_pipeline.plan
            },
            created_by="system"
        )

        return {
            "message": "Planning completed successfully",
            "pipeline_id": updated_pipeline.pipeline_id,
            "current_stage": updated_pipeline.current_stage,
            "status": updated_pipeline.status,
            "plan": updated_pipeline.plan
        }

    except ValidationError as error:
        logger.error(f"Generated plan failed validation: {error}")

        raise HTTPException(
            status_code=422,
            detail={
                "message": "Generated plan does not match PipelinePlan schema",
                "errors": error.errors()
            }
        )

    except json.JSONDecodeError as error:
        logger.error(f"LLM returned invalid JSON: {error}")

        raise HTTPException(
            status_code=422,
            detail="LLM returned invalid JSON"
        )

    except RateLimitError as error:
        logger.error(f"LLM rate limit hit: {error}")

        raise HTTPException(
            status_code=429,
            detail="The selected free LLM model is temporarily rate-limited. Try another model or retry later."
        )

    except Exception as error:
        logger.error(f"Planning failed for pipeline {pipeline_id}: {error}")

        raise HTTPException(
            status_code=500,
            detail="Planning stage failed"
        )

@router.post("/{pipeline_id}/approve")
async def approve_plan(
    pipeline_id: str,
    session: Session = Depends(get_session)
):
    pipeline_state = PipelineRepository.get_by_id(session, pipeline_id)

    if pipeline_state is None:
        raise HTTPException(
            status_code=404,
            detail="Pipeline not found"
        )

    try:
        updated_pipeline = PipelineRepository.update_status(
            session=session,
            pipeline_id=pipeline_id,
            current_stage=PipelineStage.APPROVED.value,
            status=PipelineStatus.APPROVED.value
        )

        if updated_pipeline is None:
            raise HTTPException(
                status_code=404,
                detail="Pipeline not found"
            )

        AuditService.log_event(
            session=session,
            pipeline_id=updated_pipeline.pipeline_id,
            event_type=PLAN_APPROVED,
            event_message="Implementation plan approved successfully",
            event_payload={
                "current_stage": updated_pipeline.current_stage,
                "status": updated_pipeline.status,
                "approved_plan": updated_pipeline.plan
            },
            created_by="user"
        )

        return {
            "message": "Plan approved successfully",
            "pipeline_id": updated_pipeline.pipeline_id,
            "current_stage": updated_pipeline.current_stage,
            "status": updated_pipeline.status
        }

    except HTTPException:
        raise

    except Exception as error:
        logger.error(f"Plan approval failed for pipeline {pipeline_id}: {error}")

        raise HTTPException(
            status_code=500,
            detail="Plan approval failed"
        )


@router.post("/{pipeline_id}/generate-code")
async def generate_code(
    pipeline_id: str,
    session: Session = Depends(get_session)
):
    pipeline_state = PipelineRepository.get_by_id(session, pipeline_id)

    if pipeline_state is None:
        raise HTTPException(
            status_code=404,
            detail="Pipeline not found"
        )


    if pipeline_state.plan is None:
        raise HTTPException(
            status_code=400,
            detail="Pipeline does not contain an approved plan"
        )

    if pipeline_state.current_stage != PipelineStage.APPROVED.value:
        raise HTTPException(
            status_code=400,
            detail=f"Code generation cannot start from current stage: {pipeline_state.current_stage}"
        )

    if pipeline_state.status != PipelineStatus.APPROVED.value:
        raise HTTPException(
            status_code=400,
            detail=f"Plan must be approved before code generation. Current status: {pipeline_state.status}"
        )

    try:
        generated_code = await CodegenService.generate_code(
            spec=pipeline_state.spec,
            plan=pipeline_state.plan
        )

        validated_code = CodeGenerationResult(**generated_code)

        for generated_file in validated_code.files:
            PathPolicyService.validate_generated_path(
                generated_file.path
            )

        updated_pipeline = PipelineRepository.update_generated_code(
            session=session,
            pipeline_id=pipeline_id,
            generated_code=validated_code.model_dump(),
            current_stage=PipelineStage.IMPLEMENTED.value,
            status=PipelineStatus.IMPLEMENTED.value
        )

        if updated_pipeline is None:
            raise HTTPException(
                status_code=404,
                detail="Pipeline not found"
            )

        AuditService.log_event(
            session=session,
            pipeline_id=updated_pipeline.pipeline_id,
            event_type=CODE_GENERATED,
            event_message="Code generated successfully from approved plan",
            event_payload={
                "current_stage": updated_pipeline.current_stage,
                "status": updated_pipeline.status,
                "summary": updated_pipeline.generated_code.get("summary"),
                "files": [
                    file["path"]
                    for file in updated_pipeline.generated_code.get("files", [])
                ]
            },
            created_by="system"
        )

        return {
            "message": "Code generated successfully",
            "pipeline_id": updated_pipeline.pipeline_id,
            "current_stage": updated_pipeline.current_stage,
            "status": updated_pipeline.status,
            "generated_code": updated_pipeline.generated_code
        }


    except RateLimitError as error:
        raise HTTPException(
            status_code=429,
            detail="The selected free LLM model is temporarily rate-limited. Try another model or retry later."
        ) from error

    except Exception as error:
        logger.error("Code generation failed for pipeline %s: %s", pipeline_id, error)

        raise HTTPException(
            status_code=500,
            detail="Code generation failed"
        ) from error


@router.post("/{pipeline_id}/save-code")
async def save_code(
    pipeline_id: str,
    session: Session = Depends(get_session)
):
    pipeline_state = PipelineRepository.get_by_id(session, pipeline_id)

    if pipeline_state is None:
        raise HTTPException(
            status_code=404,
            detail="Pipeline not found"
        )

    if pipeline_state.generated_code is None:
        raise HTTPException(
            status_code=400,
            detail="Pipeline does not contain generated code"
        )

    try:
        written_files = CodegenService.write_generated_files(
            pipeline_state.generated_code
        )

        AuditService.log_event(
            session=session,
            pipeline_id=pipeline_id,
            event_type=CODE_SAVED,
            event_message="Generated code saved to filesystem",
            event_payload={
                "written_files": written_files
            },
            created_by="system"
        )

        return {
            "message": "Generated code written to files successfully",
            "pipeline_id": pipeline_id,
            "written_files": written_files
        }

    except ValueError as error:
        logger.error("Code saving failed validation: %s", error)
        raise HTTPException(
            status_code=422,
            detail=str(error)
        ) from error

    except Exception as error:
        logger.error("Code saving failed for pipeline %s: %s", pipeline_id, error)

        raise HTTPException(
            status_code=500,
            detail="Code saving failed"
        ) from error


@router.post("/{pipeline_id}/generate-tests")
async def generate_tests(
    pipeline_id: str,
    session: Session = Depends(get_session)
):
    pipeline_state = PipelineRepository.get_by_id(session, pipeline_id)

    if pipeline_state is None:
        raise HTTPException(
            status_code=404,
            detail="Pipeline not found"
        )

    if pipeline_state.generated_code is None:
        raise HTTPException(
            status_code=400,
            detail="Pipeline does not contain generated code"
        )

    if pipeline_state.current_stage != PipelineStage.IMPLEMENTED.value:
        raise HTTPException(
            status_code=400,
            detail=f"Tests cannot be generated from current stage: {pipeline_state.current_stage}"
        )

    try:
        generated_tests = await TestgenService.generate_tests(
            spec=pipeline_state.spec,
            plan=pipeline_state.plan,
            generated_code=pipeline_state.generated_code
        )

        validated_tests = TestGenerationResult(**generated_tests)

        for test_file in validated_tests.files:
            PathPolicyService.validate_generated_path(test_file.path)

        written_files = CodegenService.write_generated_files(
            validated_tests.model_dump()
        )

        updated_pipeline = PipelineRepository.update_generated_tests(
            session=session,
            pipeline_id=pipeline_id,
            generated_tests=validated_tests.model_dump(),
            current_stage=PipelineStage.TESTS_GENERATED.value,
            status=PipelineStatus.TESTS_GENERATED.value
        )

        if updated_pipeline is None:
            raise HTTPException(
                status_code=404,
                detail="Pipeline not found"
            )

        AuditService.log_event(
            session=session,
            pipeline_id=updated_pipeline.pipeline_id,
            event_type=TESTS_GENERATED,
            event_message="Automated tests generated and materialized successfully",
            event_payload={
                "current_stage": updated_pipeline.current_stage,
                "status": updated_pipeline.status,
                "written_files": written_files,
                "acceptance_mapping": updated_pipeline.generated_tests.get(
                    "acceptance_mapping"
                )
            },
            created_by="system"
        )

        return {
            "message": "Tests generated successfully",
            "pipeline_id": updated_pipeline.pipeline_id,
            "current_stage": updated_pipeline.current_stage,
            "status": updated_pipeline.status,
            "generated_tests": updated_pipeline.generated_tests,
            "written_files": written_files
        }

    except ValueError as error:
        logger.error("Generated tests failed validation: %s", error)

        raise HTTPException(status_code=422, detail=str(error)) from error


    except RateLimitError as error:
        logger.error("LLM rate limit hit during test generation: %s", error)

        raise HTTPException(
            status_code=429,
            detail="The selected free LLM model is temporarily rate-limited."
        ) from error

    except Exception as error:
        logger.error("Test generation failed for pipeline %s: %s", pipeline_id, error)

        raise HTTPException(
            status_code=500,
            detail="Test generation failed"
        ) from error


@router.post("/{pipeline_id}/run-quality-check")
async def run_quality_check(
    pipeline_id: str,
    session: Session = Depends(get_session)
):
    pipeline_state = PipelineRepository.get_by_id(session, pipeline_id)

    if pipeline_state is None:
        raise HTTPException(
            status_code=404,
            detail="Pipeline not found"
        )

    if pipeline_state.generated_tests is None:
        raise HTTPException(
            status_code=400,
            detail="Pipeline does not contain generated tests"
        )

    quality_results = QualityCheckService.run_quality_gates()

    if quality_results["overall_status"] == "passed":
        next_status = PipelineStatus.QUALITY_PASSED.value
    else:
        next_status = PipelineStatus.QUALITY_FAILED.value

    updated_pipeline = PipelineRepository.update_quality_results(
        session=session,
        pipeline_id=pipeline_id,
        quality_results=quality_results,
        current_stage=PipelineStage.QUALITY_CHECKED.value,
        status=next_status
    )

    if updated_pipeline is None:
        raise HTTPException(
            status_code=404,
            detail="Pipeline not found"
        )

    event_type = (
        QUALITY_CHECK_RUN
        if quality_results["overall_status"] == "passed"
        else QUALITY_CHECK_FAILED
    )

    AuditService.log_event(
        session=session,
        pipeline_id=pipeline_id,
        event_type=event_type,
        event_message="Quality checks completed",
        event_payload=quality_results,
        created_by="system"
    )

    if quality_results["overall_status"] != "passed":
        raise HTTPException(
            status_code=409,
            detail={
                "message": "Quality checks failed",
                "quality_results": quality_results
            }
        )

    return {
        "message": "Quality checks passed",
        "pipeline_id": updated_pipeline.pipeline_id,
        "current_stage": updated_pipeline.current_stage,
        "status": updated_pipeline.status,
        "quality_results": updated_pipeline.quality_results
    }