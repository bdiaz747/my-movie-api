from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional

 

app = FastAPI()

app.title = "My app con FastAPI" # para cambiar el titulo de la documentacion con Sawgger
app.version = "0.0.1" # para cambiar el la verión de la documentacion con Sawgger

class Movie(BaseModel):
    id: Optional[int] = None
    title: str
    overview: str
    year: int
    rating: float
    category: str
    
    
movies = [
    {
		"id": 1,
		"title": "Avatar",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2009",
		"rating": 7.8,
		"category": "Acción"
	},
    {
		"id": 2,
		"title": "Avatar",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2009",
		"rating": 7.8,
		"category": "Acción"
	}
]
@app.get('/', tags = ['home']) # para cambiar la ruta

def message():
    return HTMLResponse('<h1>Helo word!</h1>')


@app.get('/movies', tags = ['movies']) # para cambiar la ruta

def get_movies():
    return movies

@app.get(f'/movies/{id}',tags = ['movies']) # para cambiar la ruta

def get_movie(id: int):
    for item in movies:
        if item['id'] == id:
            return item
    return []

@app.get(f'/movies/',tags = ['movies']) # para cambiar la ruta

def get_movies_by_category(category: str, year: int):
               
    return [ item for item in movies if item['category'] == category ]


@app.get(f'/movies/title',tags = ['movies']) # para cambiar la ruta

def get_movies_by_title(title: str):
               
    return title

@app.post('/movies', tags=['movies'])
def create_movie(movie: Movie):
    movies.append(movie)
    return movies

@app.put(f'/movies/{id}', tags=['movies'])
def update_movie(id: int, movie: Movie ):
    for item in movies: 
        if item['id'] == id:
            item['title'] = movie.title
            item['overview:'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
            return movies
        
@app.delete(f'/movies/{id}', tags=['movies'])
def delate_movie(id: int, ):
    for item in movies: 
        if item['id'] == id:
            movies.remove(item)
            return movies
            
            