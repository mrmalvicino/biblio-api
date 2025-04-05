from fastapi import APIRouter, HTTPException, status
from db.client import db_client
from models.author import Author
from schemas.author import author_schema, authors_schema
from bson import ObjectId
from bson.errors import InvalidId

router = APIRouter(prefix="/author", tags=["author"], responses={404: {"message": "No encontrado"}})

@router.get("s", response_model=list[Author], status_code=status.HTTP_200_OK)
async def authors():
    return authors_schema(db_client.authors.find())

@router.get("/{id}", response_model=Author, status_code=status.HTTP_200_OK)
async def author(id: str):
    return get_author("_id", get_object_id(id))

@router.post("/", response_model=Author, status_code=status.HTTP_201_CREATED)
async def author(author: Author):
    if (author_exists("isni", author.isni)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El autor ya existe")
    author_dict = dict(author)
    del author_dict["id"]
    id = db_client.authors.insert_one(author_dict).inserted_id
    new_author = author_schema(db_client.authors.find_one({"_id": id}))
    return Author(**new_author)

@router.put("/", response_model=Author, status_code=status.HTTP_200_OK)
async def author(author: Author):
    author_dict = dict(author)
    del author_dict["id"]
    object_id = get_object_id(author.id)
    try:
        db_client.authors.find_one_and_replace({"_id": object_id}, author_dict)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El autor no existe.")
    return get_author("_id", get_object_id(author.id))

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def author(id: str):
    found = db_client.authors.find_one_and_delete({"_id": get_object_id(id)})
    if (not found):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El autor no existe.")

def get_author(key: str, value):
    author = db_client.authors.find_one({key: value})
    if (not author):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El autor no existe.")
    return Author(**author_schema(author))

def author_exists(key: str, value):
    author = db_client.authors.find_one({key: value})
    return author is not None

def get_object_id(id: str):
    try:
        return ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID no válido")