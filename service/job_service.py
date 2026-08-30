from fastapi import HTTPException

from database import SessionLocal
from models import Job


def get_job_by_id(job_id: str):

    db = SessionLocal()

    try:
        job = (
            db.query(Job)
            .filter(Job.job_id == job_id)
            .first()
        )

        if job is None:
            raise HTTPException(
                status_code=404,
                detail="해당 작업을 찾을 수 없습니다."
            )

        return {
            "job_id": job.job_id,
            "task_type": job.task_type,
            "status": job.status,
            "input_path": job.input_path,
            "result_path": job.result_path,
            "error_message": job.error_message,
            "created_at": job.created_at,
            "started_at": job.started_at,
            "finished_at": job.finished_at
        }

    finally:
        db.close()