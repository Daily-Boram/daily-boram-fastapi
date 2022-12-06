from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from project.app import api_router

app = FastAPI()
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*']
)

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)