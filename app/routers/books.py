from fastapi import APIRouter, HTTPException, status
from db.client import db_client
from models.book import Book
from schemas.book import book_schema, books_schema
from bson import ObjectId
from bson.errors import InvalidId

router = APIRouter(prefix="/book", tags=["book"], responses={404: {"message": "No encontrado"}})

@router.get("s", response_model=list[Book], status_code=status.HTTP_200_OK)
async def books():
    return books_schema(db_client.books.find())

@router.get("/{id}", response_model=Book, status_code=status.HTTP_200_OK)
async def book(id: str):
    return get_book("_id", get_object_id(id))

@router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
async def book(book: Book):
    if (book_exists("isbn", book.isbn)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El libro ya existe")
    # Validar que todos los autores existen
    for author_id in book.authors:
        try:
            obj_id = ObjectId(author_id)
        except InvalidId:
            raise HTTPException(status_code=400, detail=f"ID de autor inválido: {author_id}")
        if not db_client.authors.find_one({"_id": obj_id}):
            raise HTTPException(status_code=404, detail=f"Autor {author_id} no encontrado")
    # Insertar el libro
    book_dict = dict(book)
    del book_dict["id"]
    book_dict["authors"] = [ObjectId(a) for a in book.authors]
    inserted_id = db_client.books.insert_one(book_dict).inserted_id
    # Actualizar cada autor con el ID del nuevo libro
    for author_id in book.authors:
        db_client.authors.update_one(
            {"_id": ObjectId(author_id)},
            {"$addToSet": {"books": inserted_id}}
        )
    # Devolver libro insertado
    new_book = db_client.books.find_one({"_id": inserted_id})
    return Book(**book_schema(new_book))

@router.put("/", response_model=Book, status_code=status.HTTP_200_OK)
async def book(book: Book):
    book_dict = dict(book)
    del book_dict["id"]
    object_id = get_object_id(book.id)
    try:
        db_client.books.find_one_and_replace({"_id": object_id}, book_dict)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El libro no existe.")
    return get_book("_id", get_object_id(book.id))

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def book(id: str):
    found = db_client.books.find_one_and_delete({"_id": get_object_id(id)})
    if (not found):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El libro no existe.")

def get_book(key: str, value):
    book = db_client.books.find_one({key: value})
    if (not book):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El libro no existe.")
    return Book(**book_schema(book))

def book_exists(key: str, value):
    book = db_client.books.find_one({key: value})
    return book is not None

def get_object_id(id: str):
    try:
        return ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID no válido")