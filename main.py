from fastapi import FastAPI

app = FastAPI()

app.title = "My app con FastAPI" # para cambiar el titulo de la documentacion con Sawgger
app.version = "0.0.1" # para cambiar el la verión de la documentacion con Sawgger

@app.get('/', tags = ['home']) # para cambiar la ruta


def message():
    return 'A dormir papilin, feliz noche'

