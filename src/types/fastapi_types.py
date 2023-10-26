from typing import List

from pydantic import BaseModel


class ImageUploadResponse(BaseModel):
    filename: str
    metadata: dict


class ErrorResponse(BaseModel):
    error: str
    filename: str


class BulkImageUploadResponse(BaseModel):
    uploaded_images: List[ImageUploadResponse]
    errors: List[ErrorResponse]


class TextUploadResponse(BaseModel):
    metadata: dict


class ImageSimilarityResponse(BaseModel):
    metadata: dict
    image: str | None


class TextSimilarityResponse(BaseModel):
    metadata: dict


class RequestText(BaseModel):
    text: str
    metadata: dict


class TextQuery(BaseModel):
    text: str
    limit: int = 10
