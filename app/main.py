from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import post, user, auth, vote

# Create the database tables if they do not exist yet on startup. Don't use if using Alembic migrations in production.
# Base.metadata.create_all(bind=engine)


"""
Production note

In real production, you usually do not run create_all() on startup.
You use Alembic migrations instead. But for learning/tutorials, it’s fine.
"""
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

# Get Root
@app.get("/")
async def root():
    return {"message": "Hello, World! "}




