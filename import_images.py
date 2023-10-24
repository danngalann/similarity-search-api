import base64
import json
from io import BytesIO

import weaviate
import os
from PIL import Image

client = weaviate.Client("http://localhost:8080")  # Replace the URL with that of your Weaviate instance


def set_up_batch():
    client.batch.configure(
        batch_size=100,
        dynamic=True,
        timeout_retries=3,
        callback=None,
    )


def import_data():
    with client.batch as batch:
        for file_path in os.listdir("./images"):
            image = Image.open("./images/" + file_path)
            buffer = BytesIO()
            image = image.convert("RGB")
            image.save(buffer, format="JPEG")
            img_b64 = base64.b64encode(buffer.getvalue()).decode()

            # The properties from our schema
            data_properties = {
                "metadata": json.dumps({
                    "filename": file_path,
                }),
                "image": img_b64,
            }

            batch.add_data_object(data_properties, "Image")


if __name__ == "__main__":
    set_up_batch()
    import_data()
