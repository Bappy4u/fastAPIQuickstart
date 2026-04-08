from pydantic import BaseModel


class FormData(BaseModel):
    username: str
    password: str


class Book(BaseModel):
    title: str
    author: str
    price: float
    description: str | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "The Great Gatsby",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "author": "John Doe",
                }
            ]
        }
    }