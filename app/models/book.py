from pydantic import BaseModel
from typing import Optional

class Book(BaseModel):
    id: Optional[str] = None
    isbn: str
    title: str
    publish_year: int
    authors: list[str]