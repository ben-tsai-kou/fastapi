from pydantic import BaseModel, Field


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(ge=1, le=5)
    complete: bool

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "this is a new todo example",
                    "description": "this is a new todo example",
                    "priority": 5,
                    "complete": False,
                }
            ]
        }
    }
