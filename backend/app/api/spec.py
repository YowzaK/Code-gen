from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from pydantic import ValidationError

from app.core.database import get_session
from app.core.logger import logger
from app.models.feature_spec import FeatureSpec
from app.services.spec_service import SpecService
from app.services.audit_service import AuditService
from app.core.event_types import SPEC_UPLOADED


router = APIRouter()


@router.post("/upload")
async def upload_spec(
    spec: FeatureSpec,
    session: Session = Depends(get_session)
):
    try:
        result = await SpecService.process_spec(spec, session)

        pipeline_id = result["pipeline_id"]

        AuditService.log_event(
            session=session,
            pipeline_id=pipeline_id,
            event_type=SPEC_UPLOADED,
            event_message="Specification uploaded and validated successfully",
            event_payload=spec.model_dump(),
            created_by="user"
        )

        return {
            "message": "Successfully uploaded spec",
            "data": result
        }

    except ValidationError as error:
        logger.error(f"Spec validation failed: {error}")

        raise HTTPException(
            status_code=422,
            detail={
                "message": "Spec validation failed",
                "errors": error.errors()
            }
        )

    except KeyError as error:
        logger.error(f"Missing expected key from spec service response: {error}")

        raise HTTPException(
            status_code=500,
            detail=f"Spec service response missing expected key: {str(error)}"
        )

    except Exception as error:
        logger.error(f"Spec upload failed: {error}")

        raise HTTPException(
            status_code=500,
            detail="Spec upload failed"
        )