from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), default="staff")  # admin / staff
    created_at = Column(DateTime, default=datetime.utcnow)


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    ma_sach = Column(String(20), unique=True, nullable=False, index=True)
    tieu_de = Column(String(200), nullable=False)
    tac_gia = Column(String(100))
    the_loai = Column(String(50))
    nam_xb = Column(Integer)
    so_luong = Column(Integer, default=1)
    mo_ta = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    borrow_records = relationship("BorrowRecord", back_populates="book")


class Reader(Base):
    __tablename__ = "readers"

    id = Column(Integer, primary_key=True, index=True)
    ma_doc_gia = Column(String(20), unique=True, nullable=False, index=True)
    ten = Column(String(100), nullable=False)
    ngay_sinh = Column(Date, nullable=True)
    gioi_tinh = Column(String(10))
    sdt = Column(String(15))
    email = Column(String(100))
    dia_chi = Column(String(200))
    cccd = Column(String(20), unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    borrow_records = relationship("BorrowRecord", back_populates="reader")


class BorrowRecord(Base):
    __tablename__ = "borrow_records"

    id = Column(Integer, primary_key=True, index=True)
    ma_phieu = Column(String(20), unique=True, nullable=False, index=True)
    reader_id = Column(Integer, ForeignKey("readers.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    ngay_muon = Column(Date, nullable=False)
    ngay_hen_tra = Column(Date, nullable=False)
    ngay_tra = Column(Date, nullable=True)   # None = chưa trả
    ghi_chu = Column(Text, nullable=True)

    reader = relationship("Reader", back_populates="borrow_records")
    book = relationship("Book", back_populates="borrow_records")

    @property
    def trang_thai(self):
        from datetime import date
        if self.ngay_tra:
            return "da_tra"
        elif self.ngay_hen_tra and date.today() > self.ngay_hen_tra:
            return "qua_han"
        return "dang_muon"
