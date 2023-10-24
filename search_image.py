import base64
import json
from io import BytesIO

import weaviate
from PIL import Image

client = weaviate.Client("http://localhost:8080")  # Replace the URL with that of your Weaviate instance

image = Image.open("target.jpg")
buffer = BytesIO()
image = image.convert("RGB")
image.save(buffer, format="JPEG")
img_b64 = base64.b64encode(buffer.getvalue()).decode()

# The properties from our schema
target_data = {
    "image": img_b64,
}

result = client.query.get("Image", ["metadata"]).with_near_image(target_data, encode=False).with_limit(2).do()

print(result)