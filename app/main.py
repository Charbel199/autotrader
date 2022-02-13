import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.api.controllers import main_router
from dotenv import load_dotenv
from app.api.middlewares import ExceptionHandlingMiddleware
load_dotenv()


app = FastAPI(version='1.0', title='AutoTrader API',
              description="AutoTrader API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# To change
app.middleware("http")(ExceptionHandlingMiddleware())

app.include_router(main_router)

if __name__ == '__main__':
    uvicorn.run('main:app', host="0.0.0.0", port=5555)
