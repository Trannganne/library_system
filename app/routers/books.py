from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import Book
from app.schemas import BookCreate, BookUpdate, BookOut

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("/", response_model=List[BookOut])
def get_books(
    q: Optional[str] = Query(None, description="Tìm theo tên hoặc tác giả"),
    the_loai: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Book)
    if q:
        query = query.filter(
            Book.tieu_de.ilike(f"%{q}%") | Book.tac_gia.ilike(f"%{q}%")
        )
    if the_loai:
        query = query.filter(Book.the_loai.ilike(f"%{the_loai}%"))
    return query.all()


@router.get("/{ma_sach}", response_model=BookOut)
def get_book(ma_sach: str, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.ma_sach == ma_sach).first()
    if not book:
        raise HTTPException(404, "Không tìm thấy sách")
    return book


@router.post("/", response_model=BookOut, status_code=201)
def create_book(payload: BookCreate, db: Session = Depends(get_db)):
    if db.query(Book).filter(Book.ma_sach == payload.ma_sach).first():
        raise HTTPException(400, "Mã sách đã tồn tại")
    book = Book(**payload.model_dump())
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


@router.put("/{ma_sach}", response_model=BookOut)
def update_book(ma_sach: str, payload: BookUpdate, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.ma_sach == ma_sach).first()
    if not book:
        raise HTTPException(404, "Không tìm thấy sách")
    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(book, field, value)
    db.commit()
    db.refresh(book)
    return book


@router.delete("/{ma_sach}", status_code=204)
def delete_book(ma_sach: str, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.ma_sach == ma_sach).first()
    if not book:
        raise HTTPException(404, "Không tìm thấy sách")
    db.delete(book)
    db.commit()
