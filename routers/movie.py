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
from schemas.movie  import Movie

movie_router = APIRouter()

class User(BaseModel):
    email: str
    password: str

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
    MovieService(db).create_movie(movie)
    return JSONResponse(status_code = 201,content = {"messege": "Película registrada"})


@movie_router.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie)-> dict:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})
    
    MovieService(db).update_movie(id, movie)
    return JSONResponse(status_code=200, content={"message": "Se ha modificado la película"})


@movie_router.delete('/movies/{id}', tags=['movies'],status_code = 200)
def delate_movie(id: int) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code = 404, content={'message' : 'No encontrado'})
    MovieService(db).deleted_movie(id)
    return JSONResponse(status_code = 200,content = {"messege": "Se ha eleminado la película "})