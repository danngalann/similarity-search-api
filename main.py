import imghdr
import json
from io import BytesIO
from typing import List
from PIL import Image as PILImage

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
from starlette import status

from src.types.fastapi_types import BulkImageUploadResponse, ImageUploadResponse, TextUploadResponse, ErrorResponse, \
    ImageSimilarityResponse, RequestText, TextQuery, TextSimilarityResponse
from src.model.Image import Image
from src.model.Text import Text
from src.repository.WeaviateRepository import WeaviateRepository

app = FastAPI()
weaviate_repository = WeaviateRepository()


def create_openapi_schema():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Similarity Search API",
        version="1.0.0",
        description="Search similar text or images",
        routes=app.routes,
    )
    openapi_schema["components"]["schemas"]["Body_upload_image_bulk_upload_image_bulk_post"]['properties']['metadata'][
        'description'] = "An object containing metadata objects indexed by filename. For example: <pre>{file1.png: {author:3}}"

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = create_openapi_schema


@app.post(
    "/upload-image",
    response_model=ImageUploadResponse,
    responses={status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse}}
)
def upload_image(file: UploadFile = File(...), metadata: str = Form(...)):
    try:
        # Validate the uploaded file
        pil_image = validate_image(file)

        image = Image(pil_image, json.loads(metadata))
        weaviate_repository.import_images([image])

        return {"filename": file.filename, "metadata": metadata}

    except HTTPException as exc:
        return {"error": str(exc.detail), "filename": file.filename}


@app.post(
    "/upload-image-bulk",
    response_model=BulkImageUploadResponse,
)
def upload_image_bulk(files: List[UploadFile] = File(...), metadata: str = Form(...)):
    uploaded_images_for_response = []
    images_for_weaviate = []
    errors = []

    metadata = json.loads(metadata)

    for file in files:
        try:
            # Validate the uploaded file
            image_metadata = metadata[file.filename]
            pil_image = validate_image(file)

            image = Image(pil_image, image_metadata)
            images_for_weaviate.append(image)

            # Add the valid image to the list
            uploaded_images_for_response.append({"filename": file.filename, "metadata": image_metadata})

        except HTTPException as exc:
            # If an invalid file is found, add it to the errors list
            errors.append({"filename": file.filename, "error": str(exc.detail)})

    weaviate_repository.import_images(images_for_weaviate)

    # Return the response with uploaded images and errors if any
    return {"uploaded_images": uploaded_images_for_response, "errors": errors}


@app.post(
    '/search-similar-images',
    response_model=List[ImageSimilarityResponse]
)
def search_similar_images(file: UploadFile = File(...), limit: int = 10, return_images: bool = False):
    try:
        # Validate the uploaded file
        pil_image = validate_image(file)

        image = Image(pil_image)

        results = weaviate_repository.get_similar_images(image, limit, return_images)

        return [{"metadata": result.metadata, "image": result.image_as_base64()} for result in results]

    except HTTPException as exc:
        # Handle the HTTP exception (e.g., not a valid image file)
        return {"error": str(exc.detail)}


@app.post(
    '/upload-text',
    response_model=TextUploadResponse
)
def upload_text(text: RequestText):
    try:
        text = Text(text.text, text.metadata)
        weaviate_repository.import_texts([text])

        return {"metadata": text.metadata_as_json()}

    except HTTPException as exc:
        # Handle the HTTP exception (e.g., not a valid image file)
        return {"error": str(exc.detail)}


@app.post(
    '/upload-text-bulk',
    response_model=List[TextUploadResponse]
)
def upload_text_bulk(texts: List[RequestText]):
    try:
        texts = [Text(text.text, text.metadata) for text in texts]
        weaviate_repository.import_texts(texts)

        return [{"metadata": text.metadata_as_json()} for text in texts]

    except HTTPException as exc:
        return {"error": str(exc.detail)}


@app.post(
    '/search-similar-texts',
    response_model=List[TextSimilarityResponse]
)
def search_similar_texts(text_query: TextQuery):
    try:
        text = Text(text_query.text, {})

        results = weaviate_repository.get_similar_texts(text, text_query.limit)

        return [{"metadata": result.metadata} for result in results]

    except HTTPException as exc:
        return {"error": str(exc.detail)}


def validate_image(file: UploadFile) -> PILImage:
    # Read the file content
    contents = file.file.read()

    # Check if the file type is a valid image (e.g., jpeg, png, gif, etc.)
    image_type = imghdr.what(None, contents)
    if image_type not in ('jpeg', 'png'):
        raise HTTPException(status_code=400,
                            detail=f"File '{file.filename}' is not a valid image. Only JPEG and PNG are supported.")

    return PILImage.open(BytesIO(contents))
