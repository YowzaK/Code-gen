from sqlmodel import Session
from app.models.pipeline_event_db import PipelineEventDB
from app.repository.pipeline_event_repository import  PipeLineEventRepository


class AuditService:

    @staticmethod
    def log_event(
        session: Session,
        pipeline_id: str,
        event_type: str,
        event_message: str,
        event_payload: dict | None = None,
        created_by: str = "system"
    ) -> PipelineEventDB:

        event = PipelineEventDB(
            pipeline_id=pipeline_id,
            event_type=event_type,
            event_message=event_message,
            event_payload=event_payload,
            created_by=created_by
        )

        return PipeLineEventRepository.create(session, event)


    @staticmethod
    def get_events(
        session:Session
    ) -> PipelineEventDB:

        return PipeLineEventRepository.list_all(session)