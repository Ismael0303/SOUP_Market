from fastapi import FastAPI
from app.database import Base, engine # Import Base and engine from database.py
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth_router, user_router
from app.routers import business_router
from app.routers import product_router
from app.routers import public_router # Import the new public router

# Create the FastAPI application instance
app = FastAPI(
    title="SOUP Emprendimientos API",
    description="API para la gestión de micro-emprendimientos y freelancers, incluyendo tiendas virtuales, productos, servicios, gestión de encargos e integración con IA.",
    version="0.1.0",
)

# Function to create database tables
# IMPORTANT: Ensure models are imported/loaded BEFORE calling Base.metadata.create_all
# Importing app.models here ensures that all declarative models are registered with Base.metadata
def create_db_tables():
    # Importing models here ensures that all model classes (like Usuario) are
    # defined and registered with Base.metadata before create_all is called.
    import app.models
    Base.metadata.create_all(bind=engine)

# Startup event handler for FastAPI application
@app.on_event("startup")
async def startup_event():
    print("Creating database tables...")
    print(f"SQLAlchemy Engine URL: {engine.url}") # Debug line
    create_db_tables() # Call the function to create database tables
    print("Database tables created.")

# Configure CORS middleware
origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint for testing the API
@app.get("/")
async def root():
    return {"message": "Welcome to SOUP Emprendimientos API!"}

# Include routers for authentication, user profile, businesses, products, and now public endpoints
app.include_router(auth_router.router, prefix="/users", tags=["Authentication"])
app.include_router(user_router.router, prefix="/profile", tags=["User Profile"])
app.include_router(business_router.router, prefix="/businesses", tags=["Businesses"])
app.include_router(product_router.router, prefix="/products", tags=["Products & Services"])
app.include_router(public_router.router, prefix="/public", tags=["Public Listing & Search"]) # Include the new public router
