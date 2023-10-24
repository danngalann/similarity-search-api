import json


class Text:
    def __init__(self, text: str, metadata: dict):
        self.text = text
        self.metadata = metadata

    def metadata_as_json(self) -> str:
        return json.dumps(self.metadata)