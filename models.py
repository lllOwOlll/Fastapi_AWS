from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Job(Base):
    __tablename__ = "jobs"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    job_id = Column(
        String(36),
        unique=True,
        nullable=False
    )

    task_type = Column(
        String(50),
        nullable=False
    )

    status = Column(
        String(20),
        nullable=False,
        default="queued"
    )

    input_path = Column(
        String(500),
        nullable=False
    )

    result_path = Column(
        String(500),
        nullable=True
    )

    error_message = Column(
        String(500),
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.now
    )

    started_at = Column(
        DateTime,
        nullable=True
    )

    finished_at = Column(
        DateTime,
        nullable=True
    )