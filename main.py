from fastapi import FastAPI

app = FastAPI()

@app.get('/')

def message():
    return 'A dormir papilin, feliz noche'

