from typing import Optional
from sqlmodel import Session, select
from app.models.pipeline_event_db import PipelineEventDB

class PipeLineEventRepository:

    @staticmethod
    def create(session: Session, event:PipelineEventDB) -> PipelineEventDB:
        session.add(event)
        session.commit()
        session.refresh(event)
        return event
    
    @staticmethod
    def get_by_id(session: Session, event_id:str) -> Optional[PipelineEventDB]:
        statement =  select(PipelineEventDB).where(
            PipelineEventDB.event_id == event_id
        )

        return session.exec(statement).first()

    @staticmethod 
    def list_all(session: Session) -> list[PipelineEventDB]:
        statement = select(PipelineEventDB)
        return list(session.exec(statement).all())
