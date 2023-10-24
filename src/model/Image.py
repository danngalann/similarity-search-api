import base64
import json
from io import BytesIO

from PIL import Image as PILImage


class Image:
    def __init__(self, image: PILImage = None, metadata=None):
        if metadata is None:
            metadata = {}

        self.metadata = metadata
        self.image = image

    def metadata_as_json(self):
        return json.dumps(self.metadata)

    def image_as_base64(self):
        buffer = BytesIO()
        image = self.image.convert("RGB")
        image.save(buffer, format="JPEG")

        return base64.b64encode(buffer.getvalue()).decode()

    @staticmethod
    def from_result(result):
        if "image" not in result:
            image = None
        else:
            image_decoded = base64.b64decode(result["image"])
            image = PILImage.open(BytesIO(image_decoded))

        return Image(
            metadata=json.loads(result["metadata"]),
            image=image
        )
