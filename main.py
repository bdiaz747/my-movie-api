from fastapi import Depends, FastAPI, Body, HTTPException, Path, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from jwt_manager import create_token, validate_token
from config.database import Session, engine, Base
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.error_handler import ErrorHandler
from middlewares.jwt_bearer import JWTBearer


app = FastAPI()

app.title = "My app con FastAPI"  # para cambiar el título de la documentación con Swagger
app.version = "0.0.1"  # para cambiar la versión de la documentación con Swagger

app.add_middleware(ErrorHandler)

Base.metadata.create_all(bind = engine)
   
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

@app.post('/login', tags=['auth'])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)




@app.get('/movies', tags=['movies'], response_model = List[Movie], status_code = 200, dependencies=[Depends(JWTBearer())])  # para cambiar la ruta
def get_movies() -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).all()
    return JSONResponse(status_code = 200,content=jsonable_encoder(result))


@app.get('/movies/{id}', tags=['movies'], response_model = Movie)  # para cambiar la ruta
def get_movie(id: int = Path(ge=1, le=200)) -> Movie:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code = 404, content={'message' : 'No encontrado'}) 
    return JSONResponse(status_code = 200,content=jsonable_encoder(result))


@app.get('/movies/', tags=['movies'], response_model = List[Movie])  # para cambiar la ruta
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.category == category).all()
    return JSONResponse(status_code = 200,content=jsonable_encoder(result))


@app.get(f'/movies/title', tags=['movies'])  # para cambiar la ruta
def get_movies_by_title(title: str):
    return title


@app.post(f'/movies', tags=['movies'], response_model = dict, status_code = 201,)
def create_movie(movie: Movie) -> dict:
    db = Session()
    new_movie = MovieModel(**movie.dict())
    db.add(new_movie)
    db.commit()
    return JSONResponse(status_code = 201,content = {"messege": "Película registrada"})


@app.put('/movies/{id}', tags=['movies'], response_model = dict, status_code = 200)
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


@app.delete('/movies/{id}', tags=['movies'],status_code = 200)
def delate_movie(id: int) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code = 404, content={'message' : 'No encontrado'})
    db.delete(result)
    db.commit()
    return JSONResponse(status_code = 200,content = {"messege": "Se ha eleminado la película "})
