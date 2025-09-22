from pydantic import BaseModel

class AnalyzeImageRequest(BaseModel):
    image_id: str
    image_url: str
