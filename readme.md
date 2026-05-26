# E-Commerce Backend API

A production-grade REST API built with Django REST Framework.

## Features
- JWT Authentication
- Product & Category Management
- Orders & Stock Management
- Advanced Filtering & Search
- Pagination
- API Documentation (Swagger)

## Tech Stack
- Python, Django, Django REST Framework
- PostgreSQL / SQLite
- JWT Authentication
- Swagger UI

## Setup
```bash
git clone <your-repo-url>
cd ecommerce_api
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/auth/register/ | Register user |
| POST | /api/auth/token/ | Get JWT token |
| GET | /api/products/ | List products |
| GET | /api/categories/ | List categories |
| POST | /api/orders/ | Create order |

## Live Demo
Coming soon...