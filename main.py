from fastapi import Depends, FastAPI, Body, HTTPException, Path, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer
from config.database import Session, engine, Base
from models.movie import Movie as MovieModel

app = FastAPI()

app.title = "My app con FastAPI"  # para cambiar el título de la documentación con Swagger
app.version = "0.0.1"  # para cambiar la versión de la documentación con Swagger

Base.metadata.create_all(bind = engine)


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@gmail.com":
            raise HTTPException(status_code=403, detail="Credenciales son invalidas")
        
    

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
    return JSONResponse(status_code = 200,content=movies)


@app.get(f'/movies/{id}', tags=['movies'], response_model = Movie, status_code = 200)  # para cambiar la ruta
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    for item in movies:
        if item["id"] == id:
            return JSONResponse(content=item)
        return JSONResponse(status_code = 404,content=[])


@app.get(f'/movies/', tags=['movies'], response_model = List[Movie])  # para cambiar la ruta
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    data = [item for item in movies if item['category'] == category]
    return JSONResponse(content = data)


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


@app.put(f'/movies/{id}', tags=['movies'], response_model = dict, status_code = 200)
def update_movie(id: int, movie: Movie) -> dict:
    for item in movies:
        if item["id"] == id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
            return JSONResponse(status_code = 200,content = {"messege": "Película mofificada"})


@app.delete(f'/movies/{id}', tags=['movies'],status_code = 200)
def delate_movie(id: int) -> dict:
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
            return JSONResponse(status_code = 200,content = {"messege": "Se ha eleminado la película "})
