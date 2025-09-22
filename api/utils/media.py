from fastapi import Request
from api.core.config import settings


def generate_image_url(request: Request, image_id: str):
    return '{host}{media_url}/{image_id}.png'.format(
        host=str(request.base_url),
        media_url=settings.MEDIA_URL,
        image_id=image_id,
    )
