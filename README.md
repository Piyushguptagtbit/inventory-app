# Inventory & Order Management System

A full-stack application built with **FastAPI**, **React**, **PostgreSQL**, and **Docker**.

## Features
- ✅ Product management with unique SKUs
- ✅ Customer management with unique emails
- ✅ Order creation with automatic stock reduction
- ✅ Insufficient stock validation
- ✅ Responsive React UI
- ✅ Dockerized with Docker Compose
- ✅ Environment variable configuration

## Tech Stack
| Layer | Technology |
|-------|-----------|
| Backend | FastAPI (Python) |
| Frontend | React 18 |
| Database | PostgreSQL 15 |
| Container | Docker + Docker Compose |
| Web Server | Nginx |

## Project Structure
```
inventory-app/
├── backend/
│   ├── main.py          # FastAPI routes
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic schemas
│   ├── crud.py          # DB operations
│   ├── database.py      # DB connection
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── api/client.js
│   │   ├── pages/Products.js
│   │   ├── pages/Customers.js
│   │   ├── pages/Orders.js
│   │   ├── App.js
│   │   └── App.css
│   ├── public/
│   ├── nginx.conf
│   └── Dockerfile
├── docker-compose.yml
└── .env.example
```

## Local Setup

### Prerequisites
- Docker & Docker Compose
- Git

### Run locally
```bash
git clone <your-repo-url>
cd inventory-app
cp .env.example .env
# Edit .env with your values
docker compose up --build
```

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Deployment Guide

### Backend – Deploy to Render (Free)
1. Go to https://render.com → New → Web Service
2. Connect your GitHub repo
3. Settings:
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add environment variable: `DATABASE_URL` (from your PostgreSQL provider)
5. For PostgreSQL, use Render's free PostgreSQL or https://neon.tech

### Frontend – Deploy to Vercel (Free)
1. Go to https://vercel.com → New Project
2. Import your GitHub repo
3. Settings:
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `build`
4. Add environment variable:
   - `REACT_APP_API_URL` = your Render backend URL (e.g. https://your-api.onrender.com)

### Docker Hub (for Docker image link)
```bash
# Build and push backend image
docker build -t yourdockerhubusername/inventory-backend:latest ./backend
docker push yourdockerhubusername/inventory-backend:latest

# Build and push frontend image
docker build -t yourdockerhubusername/inventory-frontend:latest ./frontend
docker push yourdockerhubusername/inventory-frontend:latest
```

## API Endpoints
| Method | Path | Description |
|--------|------|-------------|
| GET | /products | List all products |
| POST | /products | Create product |
| PUT | /products/{id} | Update product |
| DELETE | /products/{id} | Delete product |
| GET | /customers | List all customers |
| POST | /customers | Create customer |
| PUT | /customers/{id} | Update customer |
| DELETE | /customers/{id} | Delete customer |
| GET | /orders | List all orders |
| POST | /orders | Create order |
| GET | /orders/{id} | Get order detail |
| GET | /health | Health check |

## Business Rules
- Product SKUs must be unique
- Customer emails must be unique
- Orders automatically reduce product stock
- Orders fail if stock is insufficient
