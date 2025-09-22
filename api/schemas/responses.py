from typing import Any, Annotated

from pydantic import BaseModel, BeforeValidator


def ensure_int(value: Any) -> int:
    if isinstance(value, int):
        return value
    elif isinstance(value, str) and value.isdigit():
        return int(value)
    else:
        raise ValueError(f"Expected int-like value, got {value!r}")


class ImageResponse(BaseModel):
    image_url: str
    image_id: str


class ErrorResponse(BaseModel):
    error: str
    status_code: int


class Ingredient(BaseModel):
    name: str
    calories: Annotated[int, BeforeValidator(ensure_int)]


class RawAIResponse(BaseModel):
    raw_response: str
    error: str


class AnalyzeImageResponse(BaseModel):
    dish_name: str
    calories: Annotated[int, BeforeValidator(ensure_int)]
    protein_grams: Annotated[int, BeforeValidator(ensure_int)]
    fat_grams: Annotated[int, BeforeValidator(ensure_int)]
    carbs_grams: Annotated[int, BeforeValidator(ensure_int)]
    ingredients: list[Ingredient]

    class Config:
        extra = "forbid"
