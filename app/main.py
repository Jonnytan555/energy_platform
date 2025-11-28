from fastapi import FastAPI
from app.routers import users, auth
from app.database import engine  # <-- not used but OK to import

app = FastAPI(title="Posts API")

# Include routers
app.include_router(users.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"status": "Energy API running"}