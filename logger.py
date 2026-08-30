import json
import logging
from pathlib import Path
from datetime import datetime


class JsonFormatter(logging.Formatter):

    def format(self, record):

        log_data = {
            "timestamp": datetime.now().isoformat(),
            "level": record.levelname,
            "service": getattr(record, "service", None),
            "event": getattr(record, "event", None),
            "job_id": getattr(record, "job_id", None),
            "message": record.getMessage()
        }

        return json.dumps(
            log_data,
            ensure_ascii=False
        )


# 현재 파일 위치
BASE_DIR = Path(__file__).resolve().parent

# logs 폴더
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

# 로그 파일 경로
LOG_FILE = LOG_DIR / "worker.log"


# 콘솔 Handler
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(JsonFormatter())


# 파일 Handler
file_handler = logging.FileHandler(
    LOG_FILE,
    encoding="utf-8"
)
file_handler.setFormatter(JsonFormatter())


# Logger 생성
logger = logging.getLogger("app")
logger.setLevel(logging.INFO)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)

logger.propagate = False