from fastapi import FastAPI
import uvicorn

from src.api import api_router


app = FastAPI()
app.include_router(api_router, prefix='/api')


if __name__ == '__main__':
    uvicorn.run(app, reload=True)
