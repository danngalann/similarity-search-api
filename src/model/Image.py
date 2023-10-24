import base64
import json
from io import BytesIO

from PIL import Image as PILImage


class Image:
    def __init__(self, metadata: dict, image: PILImage):
        self.metadata = metadata
        self.image = image

    def metadata_as_json(self):
        return json.dumps(self.metadata)

    def image_as_base64(self):
        buffer = BytesIO()
        image = self.image.convert("RGB")
        image.save(buffer, format="JPEG")

        return base64.b64encode(buffer.getvalue()).decode()
