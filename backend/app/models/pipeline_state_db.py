from datetime import datetime
from typing import Optional
from uuid import uuid4
from enum import Enum
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import SQLModel, Field


class PipelineStage(str, Enum):
    VALID = "spec_valid"
    PLANNED = "spec_planned"
    IMPLEMENTED = "code_generated"
    TESTED = "tests_generated"
    QUALITY_CHECKED = "quality_checked"


class PipelineStatus(str, Enum):
    PLANNING = "waiting_for_planning"
    WAITING_FOR_PLAN_APPROVAL = "waiting_for_plan_approval"
    IMPLEMENTING = "waiting_for_implementation"
    FAILED = "failed"
    COMPLETED = "completed"


class PipelineStateDB(SQLModel, table=True):
    __tablename__ = "pipelines"

    pipeline_id: str = Field(
        default_factory=lambda: str(uuid4()),
        primary_key=True,
        index=True,
    )

    current_stage: str = Field(default=PipelineStage.VALID.value)
    status: str = Field(default=PipelineStatus.PLANNING.value)

    spec: dict = Field(
        sa_column=Column(JSONB, nullable=False)
    )

    plan: Optional[dict] = Field(
        default=None,
        sa_column=Column(JSONB, nullable=True)
    )

    generated_code: Optional[dict] = Field(
        default=None,
        sa_column=Column(JSONB, nullable=True)
    )

    generated_tests: Optional[dict] = Field(
        default=None,
        sa_column=Column(JSONB, nullable=True)
    )

    quality_results: Optional[dict] = Field(
        default=None,
        sa_column=Column(JSONB, nullable=True)
    )

    created_at: datetime = Field(default_factory=datetime.utcnow)