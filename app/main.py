from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers import auth, books, readers, borrow
import app.models

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Library Management API",
    description="REST API quản lý thư viện - sách, độc giả, phiếu mượn",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(books.router)
app.include_router(readers.router)
app.include_router(borrow.router)

@app.get("/", tags=["Health"])
def root():
    return {"message": "Library API is running 📚", "docs": "/docs"}