from typing import List
from pydantic import BaseModel, field_validator


class GeneratedFile(BaseModel):
    path: str
    content: str


class CodeGenerationResult(BaseModel):
    summary: str
    files: List[GeneratedFile]

    @field_validator("files")
    @classmethod
    def files_must_not_be_empty(cls, value):
        if not value:
            raise ValueError("Generated files list cannot be empty")

        return value