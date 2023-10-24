import weaviate

client = weaviate.Client("http://localhost:8080")  # Replace the URL with that of your Weaviate instance

schema = {
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

client.schema.delete_all()  # Delete all existing schemas
client.schema.create(schema)  # Create the schema

print(client.schema.get())  # Get the schema to test connection
