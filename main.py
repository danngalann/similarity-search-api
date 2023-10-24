import imghdr
import json
from io import BytesIO
from typing import List
from PIL import Image as PILImage

from fastapi import FastAPI, File, UploadFile, HTTPException, Form

from src.model.Image import Image
from src.repository.WeaviateRepository import WeaviateRepository

app = FastAPI()
weaviate_repository = WeaviateRepository()


@app.post("/upload-image")
def upload_image(file: UploadFile = File(...), metadata: str = Form(...)):
    try:
        # Validate the uploaded file
        pil_image = validate_image(file)

        image = Image(pil_image, json.loads(metadata))
        weaviate_repository.import_images([image])

        return {"filename": file.filename, "metadata": metadata}

    except HTTPException as exc:
        # Handle the HTTP exception (e.g., not a valid image file)
        return {"error": str(exc.detail)}


@app.post("/upload-image-bulk")
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


def validate_image(file: UploadFile) -> PILImage:
    # Read the file content
    contents = file.file.read()

    # Check if the file type is a valid image (e.g., jpeg, png, gif, etc.)
    image_type = imghdr.what(None, contents)
    if image_type not in ('jpeg', 'png'):
        raise HTTPException(status_code=400, detail=f"File '{file.filename}' is not a valid image. Only JPEG and PNG are supported.")

    return PILImage.open(BytesIO(contents))

