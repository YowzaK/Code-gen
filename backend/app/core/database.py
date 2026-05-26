from sqlmodel import SQLModel, create_engine, Session
from app.core.config import DATABASE_URL

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not configured")


engine = create_engine(
    DATABASE_URL,
    echo=True,
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session