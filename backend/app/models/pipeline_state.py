from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum
from app.models.feature_spec import FeatureSpec
from app.models.pipeline_plan import PipelinePlan

class PipelineStage(str, Enum):
    VALID = "spec_valid"
    PLANNED = "spec_planned"
    APPROVED = "spec_plan_approved"
    IMPLEMENTED = "code_generated"
    TESTED = "tests_generated"
    QUALITY_CHECKED = "quality_checked"


class PipelineStatus(str, Enum):
    PLANNING = "waiting_for_planning"
    PLANNED = "waiting_for_plan_approval"
    APPROVED= "Approved_waiting_for_approval"
    IMPLEMENTING = "waiting_for_implementation"
    FAILED = "failed"
    COMPLETED = "completed"
    

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