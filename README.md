# Inventory & Order Management System

A full-stack application built with FastAPI, React, PostgreSQL, and Docker.

## Features
-  Product management with unique SKUs
-  Customer management with unique emails
-  Order creation with automatic stock reduction
-  Insufficient stock validation
-  Responsive React UI
-  Dockerized with Docker Compose
-  Environment variable configuration

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


- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

Deployment Guide

Backend – Deploy to Render

https://inventory-backend-w6a7.onrender.com/docs

Frontend – Deploy to Vercel

inventory-app-ce31.vercel.app

 Docker Hub (for Docker image link)
https://hub.docker.com/repository/docker/piyushgupta12082002/inventory-backend/general


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

THANK YOU FOR READING THIS LONG
piyushguptagtbit
