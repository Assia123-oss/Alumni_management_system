from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from users.routes import router as users_router
from alumni.routes import router as alumni_router
# from events.routes import router as events_router
from app.core.database import Base, engine

app = FastAPI(title="Alumni Management System")
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from users.routes import router as users_router
from alumni.routes import router as alumni_router
# from events.routes import router as events_router  # Keep this commented out
from app.core.database import Base, engine

app = FastAPI()  # Remove the title for now to keep it simple

# Create database tables
Base.metadata.create_all(bind=engine)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers without prefixes (they should be defined in the router files)
app.include_router(users_router)
app.include_router(alumni_router)

@app.get("/")
def root():  # Remove async for simplicity
    return {"message": "Welcome to Alumni Management System API"}

Base.metadata.create_all(bind=engine)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with proper prefixes
app.include_router(users_router)
app.include_router(alumni_router)
# app.include_router(events_router, prefix="/events", tags=["events"])

@app.get("/")
async def root():
    return {"message": "Welcome to Alumni Management System API"}