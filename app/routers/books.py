from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/book", tags=["book"], responses={404: {"message": "No encontrado"}})

class Book(BaseModel):
    id: int
    isbn: str
    title: str
    publish_year: int

books_list: List[Book] = [
    Book(id=1, isbn="1234567890123", title="Súper libro de Física", publish_year=2020),
    Book(id=2, isbn="0987654321098", title="Robots e imperio", publish_year=1985),
    Book(id=3, isbn="4564564564564", title="De la tierra a la luna", publish_year=1969),
    Book(id=4, isbn="7777788878777", title="La vuelta al mundo en ochenta días", publish_year=1972)
]

@router.get("s", response_model=List[Book], status_code=status.HTTP_200_OK)
async def books():
    return books_list

@router.get("/{id}", response_model=Book, status_code=status.HTTP_200_OK)
async def book(id: int):
    return get_book(id)

@router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
async def book(book: Book):
    if (book_id_exists(book.id)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El libro ya existe.")
    else:
        books_list.append(book)
        return book

@router.put("/", response_model=Book, status_code=status.HTTP_200_OK)
async def book(book: Book):
    for i, saved_book in enumerate(books_list):
        if (saved_book.id == book.id):
            books_list[i] = book
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El libro no existe.")

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def book(id: int):
    for i, saved_book in enumerate(books_list):
        if (saved_book.id == id):
            del books_list[i]
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El libro no existe.")

def get_book(id: int):
    filtered_books = filter(lambda b: b.id == id, books_list)
    try:
        return list(filtered_books)[0]
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El libro no existe.")

def book_id_exists(id: int):
    filtered_books = filter(lambda b: b.id == id, books_list)
    return 0 < len(list(filtered_books))