from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import Reader
from app.schemas import ReaderCreate, ReaderUpdate, ReaderOut

router = APIRouter(prefix="/readers", tags=["Readers"])


@router.get("/", response_model=List[ReaderOut])
def get_readers(
    q: Optional[str] = Query(None, description="Tìm theo tên"),
    db: Session = Depends(get_db)
):
    query = db.query(Reader)
    if q:
        query = query.filter(Reader.ten.ilike(f"%{q}%"))
    return query.all()


@router.get("/{ma_doc_gia}", response_model=ReaderOut)
def get_reader(ma_doc_gia: str, db: Session = Depends(get_db)):
    reader = db.query(Reader).filter(Reader.ma_doc_gia == ma_doc_gia).first()
    if not reader:
        raise HTTPException(404, "Không tìm thấy độc giả")
    return reader


@router.post("/", response_model=ReaderOut, status_code=201)
def create_reader(payload: ReaderCreate, db: Session = Depends(get_db)):
    if db.query(Reader).filter(Reader.ma_doc_gia == payload.ma_doc_gia).first():
        raise HTTPException(400, "Mã độc giả đã tồn tại")
    reader = Reader(**payload.model_dump())
    db.add(reader)
    db.commit()
    db.refresh(reader)
    return reader


@router.put("/{ma_doc_gia}", response_model=ReaderOut)
def update_reader(ma_doc_gia: str, payload: ReaderUpdate, db: Session = Depends(get_db)):
    reader = db.query(Reader).filter(Reader.ma_doc_gia == ma_doc_gia).first()
    if not reader:
        raise HTTPException(404, "Không tìm thấy độc giả")
    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(reader, field, value)
    db.commit()
    db.refresh(reader)
    return reader


@router.delete("/{ma_doc_gia}", status_code=204)
def delete_reader(ma_doc_gia: str, db: Session = Depends(get_db)):
    reader = db.query(Reader).filter(Reader.ma_doc_gia == ma_doc_gia).first()
    if not reader:
        raise HTTPException(404, "Không tìm thấy độc giả")
    db.delete(reader)
    db.commit()
