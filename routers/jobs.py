from fastapi import APIRouter

from service.job_service import get_job_by_id


router = APIRouter(
    prefix="/jobs",
    tags=["jobs"]
)


@router.get("/{job_id}")
def get_job(job_id: str):
    return get_job_by_id(job_id)