# main.py
from fastapi import FastAPI
import models, database
from routers import users, posts , auth
from middlewares import LoggingMiddleware
from fastapi.responses import JSONResponse
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Blog API with JWT & RBAC")

# Create tables
models.Base.metadata.create_all(bind=database.engine)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "message": "Internal Server Error",
            "detail": str(exc),
            "path": request.url.path
        },
    )


# adding the CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)
app.add_middleware(LoggingMiddleware)

