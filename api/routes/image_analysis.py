import os
from typing import Union
from pathlib import Path
from json import loads

from openai import BadRequestError
from fastapi import APIRouter

from api.schemas.responses import AnalyzeImageResponse, ErrorResponse, RawAIResponse
from api.schemas.requests import AnalyzeImageRequest
from api.utils.ai import analyze_image_with_ai, fallback_image_analyze

router = APIRouter()


@router.post(
    '/analyze-image/',
    response_model=Union[AnalyzeImageResponse, ErrorResponse, RawAIResponse],
)
async def analyze_image(
    body: AnalyzeImageRequest,
):
    
    file_path = Path(
        os.path.abspath('./media/{filename}.png'.format(filename=body.image_id))
    )

    if not file_path.exists():
        return ErrorResponse(
            error='Image with this ID is not exists.',
            status_code=400,
        )

    try:
        response = await analyze_image_with_ai(
            image_url=body.image_url,
            expected_schema=AnalyzeImageResponse,
        )
    except BadRequestError:
        return ErrorResponse(error='Invalid AI request.', status_code=400)

    raw_response = response

    try:
        parsed_response = loads(raw_response)
        return AnalyzeImageResponse(**parsed_response)
    except Exception:
        try:
            fallback_response = await fallback_image_analyze(
                raw_response=raw_response,
                expected_schema=AnalyzeImageResponse,
            )
            parsed_response = loads(fallback_response)
            return AnalyzeImageResponse(**parsed_response)
        except Exception as exc: 
            return RawAIResponse(raw_response=raw_response, error=str(exc))
