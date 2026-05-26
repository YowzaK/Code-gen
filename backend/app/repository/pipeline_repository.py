from typing import Optional

from sqlmodel import Session, select

from app.models.pipeline_state_db import PipelineStateDB


class PipelineRepository:

    @staticmethod
    def create(session: Session, pipeline_state: PipelineStateDB) -> PipelineStateDB:
        session.add(pipeline_state)
        session.commit()
        session.refresh(pipeline_state)
        return pipeline_state

    @staticmethod
    def get_by_id(session: Session, pipeline_id: str) -> Optional[PipelineStateDB]:
        statement = select(PipelineStateDB).where(
            PipelineStateDB.pipeline_id == pipeline_id
        )

        return session.exec(statement).first()

    @staticmethod
    def update(session: Session, pipeline_state: PipelineStateDB) -> PipelineStateDB:
        session.add(pipeline_state)
        session.commit()
        session.refresh(pipeline_state)
        return pipeline_state

    @staticmethod
    def list_all(session: Session) -> list[PipelineStateDB]:
        statement = select(PipelineStateDB)
        return list(session.exec(statement).all())