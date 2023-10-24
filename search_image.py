from PIL import Image as PILImage

from src.model.Image import Image
from src.repository.WeaviateRepository import WeaviateRepository

repo = WeaviateRepository()

pil_image = PILImage.open("target.jpg")
image = Image(pil_image, {"filename": "target.jpg"})

results = repo.get_similar_images(image, limit=2)

print([result.__str__() for result in results])

