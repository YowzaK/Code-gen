from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum
from app.models.feature_spec import FeatureSpec
from app.models.pipeline_plan import PipelinePlan

class PipelineStage(Enum):
    VALID = "spec_valid"
    PLANNED = "spec_planned"

class PipelineStatus(Enum):
    PLANNING = "waiting_for_planning"
    IMPLEMENTING = "waiting_for_implementation"
    

class PipelineState(BaseModel):

    pipeline_id: str

    current_stage: PipelineStage

    status: PipelineStatus

    spec: Optional[FeatureSpec] = None

    plan: Optional[PipelinePlan] = None

    generated_code: Optional[dict] = None

    generated_tests: Optional[dict] = None

    quality_results: Optional[dict] = None

    created_at: datetime