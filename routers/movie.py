from fastapi import APIRouter
from fastapi import Depends, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService

movie_router = APIRouter()

class User(BaseModel):
    email: str
    password: str

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

@movie_router.get('/movies', tags=['movies'], response_model = List[Movie], status_code = 200, dependencies=[Depends(JWTBearer())])  # para cambiar la ruta
def get_movies() -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movies()
    return JSONResponse(status_code = 200,content=jsonable_encoder(result))


@movie_router.get('/movies/{id}', tags=['movies'], response_model = Movie)  # para cambiar la ruta
def get_movie(id: int = Path(ge=1, le=200)) -> Movie:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code = 404, content={'message' : 'No encontrado'}) 
    return JSONResponse(status_code = 200,content=jsonable_encoder(result))


@movie_router.get('/movies/', tags=['movies'], response_model = List[Movie])  # para cambiar la ruta
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    db = Session()
    result =  MovieService(db).get_movies_by_category(category)
    if not result:
        return JSONResponse(status_code = 404, content={'message' : 'No encontrado'}) 
    return JSONResponse(status_code = 200,content=jsonable_encoder(result))


@movie_router.get('/movies/title/', tags=['movies'], response_model = List[Movie])  # para cambiar la ruta
def get_movies_by_title(title: str= Query(min_length=1, max_length=45)) -> List[Movie]:
    db = Session()
    result =  MovieService(db).get_movies_by_title(title)
    if not result:
        return JSONResponse(status_code = 404, content={'message' : 'No encontrado'}) 
    return JSONResponse(status_code = 200,content=jsonable_encoder(result))



@movie_router.post(f'/movies', tags=['movies'], response_model = dict, status_code = 201,)
def create_movie(movie: Movie) -> dict:
    db = Session()
    new_movie = MovieModel(**movie.dict())
    db.add(new_movie)
    db.commit()
    return JSONResponse(status_code = 201,content = {"messege": "Película registrada"})


@movie_router.put('/movies/{id}', tags=['movies'], response_model = dict, status_code = 200)
def update_movie(id: int, movie: Movie) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code = 404, content={'message' : 'No encontrado'}) 
    result.title = movie.title
    result.overview = movie.overview
    result.year = movie.year
    result.rating = movie.rating
    result.category = movie.category
    db.commit()
    return JSONResponse(status_code = 200,content = {"messege": "Película mofificada"})


@movie_router.delete('/movies/{id}', tags=['movies'],status_code = 200)
def delate_movie(id: int) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code = 404, content={'message' : 'No encontrado'})
    db.delete(result)
    db.commit()
    return JSONResponse(status_code = 200,content = {"messege": "Se ha eleminado la película "})