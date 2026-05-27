from typing import List
from pydantic import BaseModel, field_validator


class GeneratedTestFile(BaseModel):
    path: str
    content: str


class AcceptanceTestMapping(BaseModel):
    acceptance_criterion: str
    test_name: str


class TestGenerationResult(BaseModel):
    summary: str
    files: List[GeneratedTestFile]
    acceptance_mapping: List[AcceptanceTestMapping]

    @field_validator("files")
    @classmethod
    def files_must_not_be_empty(cls, value):
        if not value:
            raise ValueError("Generated test files cannot be empty")
        return value

    @field_validator("acceptance_mapping")
    @classmethod
    def acceptance_mapping_must_not_be_empty(cls, value):
        if not value:
            raise ValueError("Acceptance mapping cannot be empty")
        return value