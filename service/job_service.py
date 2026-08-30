from pathlib import Path

from fastapi import HTTPException

from database import SessionLocal
from models import Job


def get_job_by_id(job_id: str):
    db = SessionLocal()

    try:
        job = db.query(Job).filter(
            Job.job_id == job_id
        ).first()

        if job is None:
            raise HTTPException(
                status_code=404,
                detail="존재하지 않는 작업입니다."
            )

        return {
            "job_id": job.job_id,
            "task_type": job.task_type,
            "status": job.status,
            "input_path": job.input_path,
            "result_path": job.result_path,
            "error_message": job.error_message
        }

    finally:
        db.close()


def get_job_result(job_id: str):
    db = SessionLocal()

    try:
        job = db.query(Job).filter(
            Job.job_id == job_id
        ).first()

        if job is None:
            raise HTTPException(
                status_code=404,
                detail="존재하지 않는 작업입니다."
            )

        if job.status != "completed":
            raise HTTPException(
                status_code=409,
                detail=f"아직 완료되지 않은 작업입니다. status={job.status}"
            )

        if job.result_path is None:
            raise HTTPException(
                status_code=404,
                detail="결과 파일 경로가 없습니다."
            )

        result_path = Path(job.result_path)

        if not result_path.exists():
            raise HTTPException(
                status_code=404,
                detail="결과 파일이 존재하지 않습니다."
            )

        return str(result_path)

    finally:
        db.close()