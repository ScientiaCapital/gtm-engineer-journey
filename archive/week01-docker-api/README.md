# Week 1: Docker & FastAPI Project

## Project Goal
Build a containerized FastAPI application with Neon PostgreSQL and Redis caching.

## Setup Instructions

1. **Install Dependencies**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install fastapi uvicorn sqlalchemy psycopg2-binary redis python-dotenv
```

2. **Environment Variables**
Copy `.env.example` to `.env` and add your Neon database URL:
```
DATABASE_URL=your_neon_connection_string
```

3. **Run Locally**
```bash
uvicorn main:app --reload
```

4. **Build Docker Container**
```bash
docker build -t gtm-api .
docker run -p 8000:8000 gtm-api
```

## Daily Tasks

- Monday: Docker basics, Dockerfile
- Tuesday: Docker Compose
- Wednesday: Database setup
- Thursday: Redis integration  
- Friday: Complete API
- Weekend: Deploy to Railway

## Deployment
- Push to GitHub
- Connect Railway to GitHub
- Add environment variables
- Get live URL

## Demo Requirements
- [ ] User CRUD operations
- [ ] JWT authentication
- [ ] Redis caching
- [ ] Swagger documentation
- [ ] Deployed and live
