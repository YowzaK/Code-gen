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
    def update_status(
        session: Session,
        pipeline_id: str,
        current_stage: str,
        status: str
    ) -> Optional[PipelineStateDB]:

        statement = select(PipelineStateDB).where(
            PipelineStateDB.pipeline_id == pipeline_id
        )

        pipeline_state = session.exec(statement).first()

        if pipeline_state is None:
            return None

        pipeline_state.current_stage = current_stage
        pipeline_state.status = status

        session.add(pipeline_state)
        session.commit()
        session.refresh(pipeline_state)

        return pipeline_state


    @staticmethod
    def list_all(session: Session) -> list[PipelineStateDB]:
        statement = select(PipelineStateDB)
        return list(session.exec(statement).all())

    
    @staticmethod
    def update_generated_code(
        session: Session,
        pipeline_id: str,
        generated_code: dict,
        current_stage: str,
        status: str
    ) -> Optional[PipelineStateDB]:
        statement = select(PipelineStateDB).where(
            PipelineStateDB.pipeline_id == pipeline_id
        )

        pipeline_state = session.exec(statement).first()

        if pipeline_state is None:
            return None

        pipeline_state.generated_code = generated_code
        pipeline_state.current_stage = current_stage
        pipeline_state.status = status

        session.add(pipeline_state)
        session.commit()
        session.refresh(pipeline_state)

        return pipeline_state

    @staticmethod
    def update_generated_tests(
        session: Session,
        pipeline_id: str,
        generated_tests: dict,
        current_stage: str,
        status: str
    ) -> Optional[PipelineStateDB]:

        pipeline_state = PipelineRepository.get_by_id(session, pipeline_id)

        if pipeline_state is None:
            return None

        pipeline_state.generated_tests = generated_tests
        pipeline_state.current_stage = current_stage
        pipeline_state.status = status

        session.add(pipeline_state)
        session.commit()
        session.refresh(pipeline_state)

        return pipeline_state


    @staticmethod
    def update_quality_results(
        session: Session,
        pipeline_id: str,
        quality_results: dict,
        current_stage: str,
        status: str
    ) -> Optional[PipelineStateDB]:

        pipeline_state = PipelineRepository.get_by_id(session, pipeline_id)

        if pipeline_state is None:
            return None

        pipeline_state.quality_results = quality_results
        pipeline_state.current_stage = current_stage
        pipeline_state.status = status

        session.add(pipeline_state)
        session.commit()
        session.refresh(pipeline_state)

        return pipeline_state