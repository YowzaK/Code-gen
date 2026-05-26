import uuid
from app.models.feature_spec import FeatureSpec
from app.core.logger import logger


class SpecService:

    @staticmethod
    async def process_spec(spec: FeatureSpec):

        logger.info("Processing specification")

        pipeline_id = str(uuid.uuid4())

        return {
            "pipeline_id": pipeline_id,
            "status": "validated"
        }