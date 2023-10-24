from typing import List

import weaviate

from src.model.Image import Image
from src.model.Text import Text


class WeaviateRepository:
    def __init__(self):
        self.client = weaviate.Client("http://weaviate:8080")
        self.client.batch.configure(
            batch_size=100,
            dynamic=True,
            timeout_retries=3,
            callback=None,
        )
        self.schema = {
            "classes": [
                {
                    "class": "Image",
                    "description": "An image",
                    "moduleConfig": {
                        "img2vec-neural": {
                            "imageFields": [
                                "image"
                            ]
                        }
                    },
                    "vectorIndexType": "hnsw",
                    "vectorizer": "img2vec-neural",
                    "properties": [
                        {
                            "name": "metadata",
                            "description": "Metadata of the image, in JSON format",
                            "dataType": ["string"]
                        },
                        {
                            "name": "image",
                            "description": "The image itself, in base64 format",
                            "dataType": ["blob"]
                        }
                    ],
                },
                {
                    "class": "Text",
                    "description": "A text document",
                    "moduleConfig": {
                        "text2vec-transformers": {
                            "textFields": [
                                "text"
                            ],
                            "vectorizer": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
                        }
                    },
                    "properties": [
                        {
                            "name": "metadata",
                            "description": "Metadata of the text, in JSON format",
                            "dataType": ["string"]
                        },
                        {
                            "name": "text",
                            "description": "The text itself",
                            "dataType": ["text"]
                        }
                    ]
                }
            ]
        }

    def create_schema(self):
        self.client.schema.delete_all()
        self.client.schema.create(self.schema)

    def get_schema(self) -> dict:
        return self.client.schema.get()

    def import_images(self, images: List[Image]):
        with self.client.batch as batch:
            for image in images:
                data_properties = {
                    "metadata": image.metadata_as_json(),
                    "image": image.image_as_base64(),
                }

                batch.add_data_object(data_properties, "Image")

    def import_texts(self, texts: List[Text]):
        with self.client.batch as batch:
            for text in texts:
                data_properties = {
                    "metadata": text.metadata_as_json(),
                    "text": text.text,
                }

                batch.add_data_object(data_properties, "Text")

    def get_similar_images(self, source_image: Image, limit: int = 10, return_images: bool = False) -> List[Image]:
        properties_to_get = ["metadata", "image"] if return_images else ["metadata"]

        source_image_dict = {
            "image": source_image.image_as_base64(),
        }
        result = (self.client.query.get("Image", properties_to_get)
                  .with_near_image(source_image_dict, encode=False)
                  .with_limit(limit)
                  .do())

        return [Image.from_result(r) for r in result["data"]["Get"]["Image"]]

    def get_similar_texts(self, source_text: Text, limit: int = 10) -> List[Text]:
        source_text_dict = {
            "text": source_text.text,
        }
        result = (self.client.query.get("Text", ["metadata"])
                  .with_near_text(source_text_dict, encode=False)
                  .with_limit(limit)
                  .do())

        return [Text.from_result(r) for r in result["data"]["Get"]["Text"]]
