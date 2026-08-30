from fastapi import APIRouter
from fastapi.responses import FileResponse

from service.job_service import get_job_by_id, get_job_result


router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("/{job_id}")
def get_job(job_id: str):
    return get_job_by_id(job_id)


@router.get("/{job_id}/result")
def get_result(job_id: str):
    result_path = get_job_result(job_id)

    return FileResponse(
        path=result_path,
        media_type="image/png",
        filename=f"{job_id}.png"
    )