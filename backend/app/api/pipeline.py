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
        logger.info(f"Starting planning stage for pipeline: {pipeline_id}")

        generated_plan = await PlannerService.generate_plan(
            pipeline_state.spec
        )

        validated_plan = PipelinePlan(**generated_plan)

        pipeline_state.plan = validated_plan.model_dump()
        pipeline_state.current_stage = PipelineStage.PLANNED.value
        pipeline_state.status = PipelineStatus.WAITING_FOR_PLAN_APPROVAL.value

        updated_pipeline = PipelineRepository.update(
            session=session,
            pipeline_state=pipeline_state
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

        pipeline_state.status = PipelineStatus.FAILED.value
        PipelineRepository.update(
            session=session,
            pipeline_state=pipeline_state
        )

        raise HTTPException(
            status_code=422,
            detail={
                "message": "Generated plan does not match PipelinePlan schema",
                "errors": error.errors()
            }
        )

    except json.JSONDecodeError as error:
        logger.error(f"LLM returned invalid JSON: {error}")

        pipeline_state.status = PipelineStatus.FAILED
        PipelineRepository.update(
            session=session,
            pipeline_state=pipeline_state
        )

        raise HTTPException(
            status_code=422,
            detail="LLM returned invalid JSON"
        )

    except RateLimitError as error:
        logger.error(f"LLM rate limit hit: {error}")

        pipeline_state.status = PipelineStatus.FAILED.value
        PipelineRepository.update(
            session=session,
            pipeline_state=pipeline_state
        )

        raise HTTPException(
            status_code=429,
            detail="The selected free LLM model is temporarily rate-limited. Try another model or retry later."
        )

    except Exception as error:
        logger.error(f"Planning failed for pipeline {pipeline_id}: {error}")

        pipeline_state.status = PipelineStatus.FAILED
        PipelineRepository.update(
            session=session,
            pipeline_state=pipeline_state
        )

        raise HTTPException(
            status_code=500,
            detail="Planning stage failed"
        )