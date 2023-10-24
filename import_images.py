import os
from PIL import Image as PILImage

from src.model.Image import Image
from src.repository.WeaviateRepository import WeaviateRepository

repository = WeaviateRepository()


def import_data():
    images = []
    for file_path in os.listdir("./images"):
        pil_image = PILImage.open("./images/" + file_path)
        image = Image(pil_image, {"filename": file_path})
        images.append(image)

    repository.import_images(images)


if __name__ == "__main__":
    repository.create_schema()
    import_data()
