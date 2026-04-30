from pydantic import BaseModel, Field, field_validator
from typing import List
import datetime

class Genre(BaseModel):
    name: str

class MovieResponse(BaseModel):
    id: int
    name: str
    description: str
    genreId: int
    imageUrl: str
    price: int
    rating: float = Field(ge=0, le=5)
    location: str
    published: bool
    createdAt: str = Field(description="ISO 8601 datetime")
    genre: Genre

    @field_validator("createdAt")
    def validate_created_at(cls, value: str) -> str:
        try:
            datetime.datetime.fromisoformat(value)
        except ValueError:
            raise ValueError("Некорректный формат даты и времени. Ожидается формат ISO 8601.")
        return value

class MoviesListResponse(BaseModel):
    movies: List[MovieResponse]
    count: int
    page: int
    pageSize: int
    pageCount: int
