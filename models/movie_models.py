from pydantic import BaseModel
from typing import List, Optional

class Genre(BaseModel):
    name: str

class MovieResponse(BaseModel):
    id: int
    name: str
    description: str
    genreId: int
    imageUrl: Optional[str]
    price: int
    rating: int
    location: str
    published: bool
    createdAt: str
    genre: Genre

class MoviesListResponse(BaseModel):
    movies: List[MovieResponse]
    count: int
    page: int
    pageSize: int
    pageCount: int
