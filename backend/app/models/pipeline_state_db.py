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


class PipelineStatus(str, Enum):
    PLANNING = "waiting_for_planning"
    IMPLEMENTING = "waiting_for_implementation"


class PipelineStateDB(SQLModel, table=True):
    __tablename__ = "pipeline_states"

    pipeline_id: str = Field(
        default_factory=lambda: str(uuid4()),
        primary_key=True,
        index=True,
    )

    current_stage: PipelineStage = Field(default=PipelineStage.VALID)
    status: PipelineStatus = Field(default=PipelineStatus.PLANNING)

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