import os
from pathlib import Path
from uuid import uuid4

from aiofiles import open as async_open
from fastapi import APIRouter, File, Request, UploadFile


from api.schemas.responses import ErrorResponse, ImageResponse
from api.utils.media import generate_image_url
from api.core.config import settings


router = APIRouter()

@router.post('/upload-photo/', response_model=ImageResponse | ErrorResponse)
async def upload_photo(
    request: Request,
    image: UploadFile = File(...),
):
    if not image.content_type.startswith('image/'): # type: ignore
        return ErrorResponse(error='Resource handles only images', status_code=415)
    
    content = await image.read()

    image_id = str(uuid4())

    file_path = Path(
        os.path.abspath('./{media_root}/{filename}.png'.format(
            media_root=settings.MEDIA_ROOT,
            filename=image_id,
            ),
        ),
    )
    file_path.parent.mkdir(parents=True, exist_ok=True)

    async with async_open(file_path, mode='wb+') as local_file:
        await local_file.write(content)
    
    image_url = generate_image_url(
        request=request,
        image_id=image_id,
    )

    return ImageResponse(image_url=image_url, image_id=image_id)
