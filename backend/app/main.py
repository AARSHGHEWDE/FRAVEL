from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routes import trips, auth, sse


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(title="FRAVEL API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(trips.router)
app.include_router(auth.router)
app.include_router(sse.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
