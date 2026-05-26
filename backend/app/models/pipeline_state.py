from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum
from app.models.feature_spec import FeatureSpec

class PipelineStage(Enum):
    VALID = "spec_valid"

class PipelineStatus(Enum):
    PLANNING = "waiting_for_planning"
    

class PipelineState(BaseModel):

    pipeline_id: str

    current_stage: PipelineStage

    status: PipelineStatus

    spec: Optional[FeatureSpec] = None

    plan: Optional[dict] = None

    generated_code: Optional[dict] = None

    generated_tests: Optional[dict] = None

    quality_results: Optional[dict] = None

    created_at: datetime