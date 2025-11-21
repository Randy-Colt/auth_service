from fastapi import FastAPI
import uvicorn

from src.api.auth_handlers import api_router


app = FastAPI()
app.include_router(api_router, prefix='/api')


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
