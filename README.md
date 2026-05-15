# 📚 Library Management REST API

A RESTful API for managing a library system — books, readers, and borrow records — built with **FastAPI** and **PostgreSQL**.

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11 |
| Framework | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Auth | JWT (python-jose + passlib) |

## 📋 Features

- **Authentication**: Register & login with JWT
- **Books**: Full CRUD + search by title/author/genre
- **Readers**: Full CRUD + search by name
- **Borrow Management**: Borrow, return, overdue tracking
- **Auto docs**: Swagger UI at `/docs`

## 🚀 Getting Started

### 1. Clone & install

```bash
git clone https://github.com/Trannganne/library_system.git
cd library-api
```

### 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```
## 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup environment

```bash
cp .env.example .env
#Update PostgreSQL configuration inside .env.
# Example:

```

### 3. Create PostgreSQL database

```sql
CREATE DATABASE library_db;
```

### 4. Run the server

```bash
uvicorn app.main:app --reload
```

Visit **http://localhost:8000/docs** for interactive API documentation.

### 5. Run UI
```Open library-ui.htmml in your browser.
Frontend communicates directly with FastAPI backend.
```

## 📁 Project Structure

```
library-api/
├── app/
│   ├── main.py           # Entry point
│   ├── database.py       # DB connection & session
│   ├── models/           # SQLAlchemy ORM models
│   ├── schemas/          # Pydantic request/response schemas
│   ├── routers/          # API route handlers
│   └── core/     
├── images/      
├── library-ui.html        # Frontend interface
├── requirements.txt
├── .env.example
└── README.md

```

## 🔗 API Endpoints

### Auth
| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Đăng ký tài khoản |
| POST | `/auth/login` | Đăng nhập, nhận JWT |

### Books
| Method | Endpoint | Description |
|---|---|---|
| GET | `/books?q=&the_loai=` | Danh sách sách, tìm kiếm |
| GET | `/books/{ma_sach}` | Chi tiết sách |
| POST | `/books` | Thêm sách mới |
| PUT | `/books/{ma_sach}` | Cập nhật sách |
| DELETE | `/books/{ma_sach}` | Xóa sách |

### Readers
| Method | Endpoint | Description |
|---|---|---|
| GET | `/readers?q=` | Danh sách độc giả |
| GET | `/readers/{ma_doc_gia}` | Chi tiết độc giả |
| POST | `/readers` | Thêm độc giả |
| PUT | `/readers/{ma_doc_gia}` | Cập nhật độc giả |
| DELETE | `/readers/{ma_doc_gia}` | Xóa độc giả |

### Borrow
| Method | Endpoint | Description |
|---|---|---|
| GET | `/borrow` | Tất cả phiếu mượn |
| GET | `/borrow/overdue` | Sách quá hạn chưa trả |
| GET | `/borrow/reader/{ma_doc_gia}` | Lịch sử mượn theo độc giả |
| POST | `/borrow` | Tạo phiếu mượn |
| PATCH | `/borrow/return` | Trả sách |
