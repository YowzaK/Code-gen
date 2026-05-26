from pydantic import BaseModel 
from typing import List 

class FeatureSpec(BaseModel):
    objective: str
    user_story: str
    business_rules: List[str]
    acceptance_criteria: List[str]
    non_functional_requirements: List[str]
    out_of_scope: List[str]