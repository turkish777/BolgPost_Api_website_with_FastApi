# main.py
from fastapi import FastAPI
import models, database
from routers import users, posts , auth

app = FastAPI(title="Blog API with JWT & RBAC")

# Create tables
models.Base.metadata.create_all(bind=database.engine)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)
