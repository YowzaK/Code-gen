from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.core.logger import logger

from app.core.database import get_session
from app.repository.pipeline_repository import PipelineRepository

router = APIRouter()

@router.get("/")
async def get_all_pipelines(
    session: Session = Depends(get_session)
):
    pipelines = PipelineRepository.list_all(session)

    if pipelines is None:
        raise HTTPException(
            status_code=404,
            detail="No development pipelines created"
        )

    return pipelines



@router.get("/{pipeline_id}")
async def get_pipeline_by__id(
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