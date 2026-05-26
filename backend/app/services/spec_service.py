import uuid

from pydantic.type_adapter import P
from app.models.feature_spec import FeatureSpec
from app.core.logger import logger
from datetime import datetime, timezone
from app.models.pipeline_state import PipelineState
from app.core.pipeline_store import PIPELINE_STORE
from app.models.pipeline_state import PipelineStage 
from app.models.pipeline_state import PipelineStatus 


class SpecService:

    @staticmethod
    async def process_spec(spec: FeatureSpec):
        pipeline_id = str(uuid.uuid4())

        # NTR
        logger.info("Processing specification")

        pipeline_state = PipelineState(
            pipeline_id=pipeline_id,
            current_stage= PipelineStage.VALID,
            status=  PipelineStatus.PLANNING,
            spec= spec,
            created_at=datetime.now(timezone.utc)
        )

        PIPELINE_STORE[pipeline_id] = pipeline_state      

    
        return {
            "pipeline_id": pipeline_id,
            "status": "validated",
        }