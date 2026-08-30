from pathlib import Path

import cv2
import redis

from database import SessionLocal
from models import Job
from logger import logger

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True,
    socket_timeout=None
)

BASE_DIR = Path(__file__).resolve().parent
RESULT_DIR = BASE_DIR / "results"
RESULT_DIR.mkdir(exist_ok=True)


print("Redis 연결 확인:", redis_client.ping())
logger.info(
    "Worker 시작",
    extra={
        "service": "worker",
        "event": "worker_started",
        "job_id": None
    }
)

while True:
    print("작업 대기 중...")

    result = redis_client.blpop(
        "job_queue",
        timeout=5
    )

    if result is None:
        continue
    queue_name, job_id = result
    logger.info(
        "Redis에서 작업 수신",
        extra={
            "service": "worker",
            "event": "job_received",
            "job_id": job_id
        }
    )
    


    db = SessionLocal()
    job = None
    try:
        job = db.query(Job).filter(Job.job_id == job_id).first()

        if job is None:
            print("MySQL에 존재하지 않는 job:", job_id)
            continue

        print("작업 조회 성공")
        print("job_id:", job.job_id)
        print("task_type:", job.task_type)
        print("status:", job.status)
        print("input_path:", job.input_path)

        # 작업 시작
        job.status = "processing"
        db.commit()

        logger.info(
            "작업 처리 시작",
            extra={
                "service": "worker",
                "event": "job_processing",
                "job_id": job_id
            }
        )

        # 원본 이미지 읽기
        image = cv2.imread(job.input_path)

        if image is None:
            raise ValueError("이미지를 읽을 수 없습니다.")

        # Grayscale 변환
        gray_image = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        # 결과 파일 경로
        result_path = RESULT_DIR / f"{job_id}.png"

        # 결과 이미지 저장
        success = cv2.imwrite(
            str(result_path),
            gray_image
        )

        if not success:
            raise ValueError("결과 이미지를 저장할 수 없습니다.")

        # 작업 완료
        job.status = "completed"
        job.result_path = str(result_path)

        db.commit()

        logger.info(
            "작업 완료",
            extra={
                "service": "worker",
                "event": "job_completed",
                "job_id": job_id
            }
        )

    except Exception as e:
        db.rollback()

        logger.error(
            f"작업 실패: {e}",
            extra={
                "service": "worker",
                "event": "job_failed",
                "job_id": job_id
            }
        )

        if job is not None:
            job.status = "failed"
            job.error_message = str(e)
            db.commit()

    finally:
        db.close()