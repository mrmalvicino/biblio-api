from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/author", tags=["author"], responses={404: {"message": "No encontrado"}})

class Author(BaseModel):
    id: int
    name: str

authors_list: List[Author] = [
    Author(id=1, name="Malvicino, Maximiliano"),
    Author(id=2, name="Bosio, Federico"),
    Author(id=3, name="Verne, Julio"),
    Author(id=3, name="Asimov, Isaac")
]

@router.get("s", response_model=List[Author], status_code=status.HTTP_200_OK)
async def authors():
    return authors_list

@router.get("/{id}", response_model=Author, status_code=status.HTTP_200_OK)
async def author(id: int):
    return get_author(id)

@router.post("/", response_model=Author, status_code=status.HTTP_201_CREATED)
async def author(author: Author):
    if (author_id_exists(author.id)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El autor ya existe.")
    else:
        authors_list.append(author)
        return author

@router.put("/", response_model=Author, status_code=status.HTTP_200_OK)
async def author(author: Author):
    for i, saved_author in enumerate(authors_list):
        if (saved_author.id == author.id):
            authors_list[i] = author
            return author
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El autor no existe.")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def author(id: int):
    for i, saved_author in enumerate(authors_list):
        if (saved_author.id == id):
            del authors_list[i]
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El autor no existe.")

def get_author(id: int):
    filtered_authors = filter(lambda b: b.id == id, authors_list)
    try:
        return list(filtered_authors)[0]
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El libro no existe.")

def author_id_exists(id: int):
    filtered_authors = filter(lambda b: b.id == id, authors_list)
    return 0 < len(list(filtered_authors))