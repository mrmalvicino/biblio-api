from pydantic import BaseModel
from typing import Optional

class Author(BaseModel):
    id: Optional[str] = None
    isni: str
    name: str