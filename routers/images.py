from fastapi import APIRouter, UploadFile, File

from service.image_service import create_grayscale_job


router = APIRouter(
    prefix="/images",
    tags=["images"]
)


@router.post("/grayscale")
async def grayscale_image(
    image: UploadFile = File(...)
):
    return await create_grayscale_job(image)