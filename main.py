from fastapi import FastAPI, UploadFile, File, HTTPException
from pathlib import Path
import uuid

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent

UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)


@app.post("/images/grayscale")
async def grayscale_image(
    image: UploadFile = File(...)
):
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
    print("job_id: ",job_id)

    # 확장자 가져오기
    suffix = Path(image.filename).suffix
    print("suffix: ",suffix)

    # 저장할 파일 경로
    input_path = UPLOAD_DIR / f"{job_id}{suffix}"
    print("input_path: ",input_path)

    # 업로드된 파일 읽기
    contents = await image.read()

    # 서버에 원본 이미지 저장
    with open(input_path, "wb") as file:
        file.write(contents)

    return {
        "job_id": job_id,
        "status": "queued",
        "input_path": str(input_path)
    }