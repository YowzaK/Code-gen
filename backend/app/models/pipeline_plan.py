from pydantic import BaseModel
from typing import List


class PipelinePlan(BaseModel):
    implementation_tasks: List[str]
    technical_design_summary: str
    impacted_files: List[str]
    risk_considerations: List[str]
    test_strategy: List[str]