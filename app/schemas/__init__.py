from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional


# ---------- USER ----------
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: Optional[str] = "staff"

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    role: str
    created_at: datetime
    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ---------- BOOK ----------
class BookCreate(BaseModel):
    ma_sach: str
    tieu_de: str
    tac_gia: Optional[str] = None
    the_loai: Optional[str] = None
    nam_xb: Optional[int] = None
    so_luong: Optional[int] = 1
    mo_ta: Optional[str] = None

class BookUpdate(BaseModel):
    tieu_de: Optional[str] = None
    tac_gia: Optional[str] = None
    the_loai: Optional[str] = None
    nam_xb: Optional[int] = None
    so_luong: Optional[int] = None
    mo_ta: Optional[str] = None

class BookOut(BaseModel):
    id: int
    ma_sach: str
    tieu_de: str
    tac_gia: Optional[str]
    the_loai: Optional[str]
    nam_xb: Optional[int]
    so_luong: int
    mo_ta: Optional[str]
    class Config:
        from_attributes = True


# ---------- READER ----------
class ReaderCreate(BaseModel):
    ma_doc_gia: str
    ten: str
    ngay_sinh: Optional[date] = None
    gioi_tinh: Optional[str] = None
    sdt: Optional[str] = None
    email: Optional[str] = None
    dia_chi: Optional[str] = None
    cccd: Optional[str] = None

class ReaderUpdate(BaseModel):
    ten: Optional[str] = None
    ngay_sinh: Optional[date] = None
    gioi_tinh: Optional[str] = None
    sdt: Optional[str] = None
    email: Optional[str] = None
    dia_chi: Optional[str] = None

class ReaderOut(BaseModel):
    id: int
    ma_doc_gia: str
    ten: str
    ngay_sinh: Optional[date]
    gioi_tinh: Optional[str]
    sdt: Optional[str]
    email: Optional[str]
    dia_chi: Optional[str]
    cccd: Optional[str]
    class Config:
        from_attributes = True


# ---------- BORROW ----------
class BorrowCreate(BaseModel):
    ma_phieu: str
    ma_doc_gia: str
    ma_sach: str
    ngay_muon: date
    ngay_hen_tra: date
    ghi_chu: Optional[str] = None

class ReturnBook(BaseModel):
    ma_phieu: str
    ngay_tra: date

class BorrowOut(BaseModel):
    id: int
    ma_phieu: str
    ngay_muon: date
    ngay_hen_tra: date
    ngay_tra: Optional[date]
    trang_thai: str
    ghi_chu: Optional[str]
    reader: ReaderOut
    book: BookOut
    class Config:
        from_attributes = True
