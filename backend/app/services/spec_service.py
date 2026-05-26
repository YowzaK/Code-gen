from app.models.feature_spec import FeatureSpec
from app.models.pipeline_state import PipelineStage 
from app.models.pipeline_state import PipelineStatus
from app.models.pipeline_state_db import (
    PipelineStateDB,
    PipelineStage,
    PipelineStatus,
)
from app.repository.pipeline_repository import PipelineRepository

class SpecService:

    @staticmethod
    async def process_spec(spec: FeatureSpec, session):

        pipeline_state = PipelineStateDB(
            current_stage=PipelineStage.VALID,
            status=PipelineStatus.PLANNING,
            spec=spec.model_dump(),
        )

        saved_pipeline = PipelineRepository.create(
            session=session,
            pipeline_state=pipeline_state
        )

        return {
            "pipeline_id": saved_pipeline.pipeline_id,
            "submitted_time": saved_pipeline.created_at,
            "current_stage": saved_pipeline.current_stage,
            "status": saved_pipeline.status
        }