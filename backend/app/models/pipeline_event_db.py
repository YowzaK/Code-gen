from datetime import datetime
from typing import Optional
from uuid import uuid4
from enum import Enum
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import ForeignKey, SQLModel, Field
from datetime import datetime, timezone

class PipelineEventDB(SQLModel, table=True):
    _tablename_ = ""

    event_id: str = Field(
        default_factory=lambda: str(uuid4()),
        primary_key=True,
        index=True,
    )

    pipeline_id: str = Field(
        sa_column=Column(
            ForeignKey("pipelines.pipeline_id"),
            nullable=False,
            index=True
        )
    )

    event_type: str
    event_message: str

    event_payload: Optional[dict] = Field(
        default=None,
        sa_column=Column(JSONB, nullable=True)
    )

    created_by: Optional[str] = "system"

    created_at: datetime = Field(
    default_factory=lambda: datetime.now(timezone.utc)
)