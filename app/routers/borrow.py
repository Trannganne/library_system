from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from app.database import get_db
from app.models import BorrowRecord, Book, Reader
from app.schemas import BorrowCreate, ReturnBook, BorrowOut

router = APIRouter(prefix="/borrow", tags=["Borrow"])


@router.get("/", response_model=List[BorrowOut])
def get_all_borrows(db: Session = Depends(get_db)):
    return db.query(BorrowRecord).all()


@router.get("/overdue", response_model=List[BorrowOut])
def get_overdue(db: Session = Depends(get_db)):
    today = date.today()
    return db.query(BorrowRecord).filter(
        BorrowRecord.ngay_tra == None,
        BorrowRecord.ngay_hen_tra < today
    ).all()


@router.get("/reader/{ma_doc_gia}", response_model=List[BorrowOut])
def get_by_reader(ma_doc_gia: str, db: Session = Depends(get_db)):
    reader = db.query(Reader).filter(Reader.ma_doc_gia == ma_doc_gia).first()
    if not reader:
        raise HTTPException(404, "Không tìm thấy độc giả")
    return db.query(BorrowRecord).filter(BorrowRecord.reader_id == reader.id).all()


@router.post("/", response_model=BorrowOut, status_code=201)
def borrow_book(payload: BorrowCreate, db: Session = Depends(get_db)):
    if db.query(BorrowRecord).filter(BorrowRecord.ma_phieu == payload.ma_phieu).first():
        raise HTTPException(400, "Mã phiếu đã tồn tại")

    reader = db.query(Reader).filter(Reader.ma_doc_gia == payload.ma_doc_gia).first()
    if not reader:
        raise HTTPException(404, "Không tìm thấy độc giả")

    book = db.query(Book).filter(Book.ma_sach == payload.ma_sach).first()
    if not book:
        raise HTTPException(404, "Không tìm thấy sách")
    if book.so_luong < 1:
        raise HTTPException(400, "Sách đã hết, không thể mượn")

    record = BorrowRecord(
        ma_phieu=payload.ma_phieu,
        reader_id=reader.id,
        book_id=book.id,
        ngay_muon=payload.ngay_muon,
        ngay_hen_tra=payload.ngay_hen_tra,
        ghi_chu=payload.ghi_chu,
    )
    book.so_luong -= 1
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.patch("/return", response_model=BorrowOut)
def return_book(payload: ReturnBook, db: Session = Depends(get_db)):
    record = db.query(BorrowRecord).filter(BorrowRecord.ma_phieu == payload.ma_phieu).first()
    if not record:
        raise HTTPException(404, "Không tìm thấy phiếu mượn")
    if record.ngay_tra:
        raise HTTPException(400, "Sách đã được trả rồi")

    record.ngay_tra = payload.ngay_tra
    record.book.so_luong += 1
    db.commit()
    db.refresh(record)
    return record
