from pathlib import Path
import uuid

from fastapi import UploadFile, HTTPException

from database import SessionLocal
from models import Job

from redis_client import redis_client


BASE_DIR = Path(__file__).resolve().parent.parent

UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)


async def create_grayscale_job(image: UploadFile):

    # 이미지 파일인지 확인
    if image.content_type not in [
        "image/jpeg",
        "image/png"
    ]:
        raise HTTPException(
            status_code=400,
            detail="JPEG 또는 PNG 이미지만 업로드할 수 있습니다."
        )

    # 작업 ID 생성
    job_id = str(uuid.uuid4())

    # 원본 파일 확장자
    suffix = Path(image.filename).suffix

    # 이미지 저장 경로
    input_path = UPLOAD_DIR / f"{job_id}{suffix}"

    # 업로드 이미지 읽기
    contents = await image.read()

    # 원본 이미지 저장
    with open(input_path, "wb") as file:
        file.write(contents)

    # DB Session 생성
    db = SessionLocal()

    try:
        new_job = Job(
            job_id=job_id,
            task_type="grayscale",
            status="queued",
            input_path=str(input_path)
        )

        db.add(new_job)
        db.commit()
        redis_client.rpush("job_queue", job_id)

    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="작업 정보를 DB에 저장하지 못했습니다."
        )

    finally:
        db.close()

    return {
        "job_id": job_id,
        "status": "queued"
    }