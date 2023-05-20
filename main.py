from dataclasses import Field
from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

app.title = "My app con FastAPI"  # para cambiar el título de la documentación con Swagger
app.version = "0.0.1"  # para cambiar la versión de la documentación con Swagger

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=1, max_length=15)
    overview: str = Field(min_length=15, max_length=50)
    year: int = Field(default=2022, le=2023)
    rating: float = Field(ge=1, le=10)
    category: str = Field(min_length=5, max_length=15)

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Titulo Nuevo",
                "overview": "Descripción corta",
                "year": 2022,
                "rating": 9.8,
                "category": "Acción"
            }
        }


movies = [
    {
        "id": 1,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        "year": 2009,
        "rating": 7.8,
        "category": "Acción"
    },
    {
        "id": 2,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        "year": 2009,
        "rating": 7.8,
        "category": "Acción"
    }
]


@app.get('/', tags=['home'])  # para cambiar la ruta
def message():
    return HTMLResponse('<h1>Hello Word</h1>')


@app.get('/movies', tags=['movies'])  # para cambiar la ruta
def get_movies():
    return JSONResponse(content=movies)


@app.get(f'/movies/{id}', tags=['movies'])  # para cambiar la ruta
def get_movie(id: int = Path(ge=1, le=2000)):
    for item in movies:
        if item["id"] == id:
            return JSONResponse(content=item)
    return JSONResponse(content=[])


@app.get(f'/movies/', tags=['movies'])  # para cambiar la ruta
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)):
    return [item for item in movies if item['category'] == category]


@app.get(f'/movies/title', tags=['movies'])  # para cambiar la ruta
def get_movies_by_title(title: str):
    return title


@app.post(f'/movies', tags=['movies'])
def create_movie(movie: Movie):
    movies.append(movie)
    return movies


@app.put(f'/movies/{id}', tags=['movies'])
def update_movie(id: int, movie: Movie):
    for item in movies:
        if item["id"] == id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
            return movies


@app.delete(f'/movies/{id}', tags=['movies'])
def delate_movie(id: int):
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
            return movies
