# Nexus ProDev E-Commerce Backend

## Project Overview
This repository contains the backend system for a scalable, high-performance E-Commerce platform. Built as the capstone project for the **ALX ProDev Backend Engineering** program, this system demonstrates advanced backend methodologies, including professional database design, secure authentication, and containerized deployment.

### Key Goals
- **Scalability:** Optimized PostgreSQL schema for large product catalogs.
- **Security:** Bulletproof authentication using JWT (JSON Web Tokens).
- **Documentation:** Interactive API reference using Swagger/OpenAPI.
- **Performance:** Efficient querying with indexing and pagination.

---

## Tech Stack
- **Framework:** Django 5.0 + Django REST Framework (DRF)
- **Database:** PostgreSQL (Relational)
- **Security:** SimpleJWT (Authentication)
- **DevOps:** Docker & Docker Compose
- **API Docs:** drf-spectacular (Swagger UI)

---

## Getting Started (Docker)
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/](https://github.com/)[YOUR_USERNAME]/alx-project-nexus.git
   cd alx-project-nexus

ecommerce-backend/
├── docker/
│   └── entrypoint.sh
├── src/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── asgi.py
│   │   └── wsgi.py
│   ├── users/
│   │   ├── migrations/
│   │   ├── models.py
│   │   ├── admin.py
│   │   └── apps.py
│   └── manage.py
├── .env
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md

