from fastapi import FastAPI
from app.database import Base, engine # Import Base and engine from database.py
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth_router, user_router
from app.routers import business_router
from app.routers import product_router
from app.routers import public_router
from app.routers import insumo_router # Import the new insumo router
from app.routers import public_ai_router
from app.routers import plugin_router # Import the new plugin router
from app.routers import venta_router # Import the new venta router
from app.routers import niam_router # Import the new niam router

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
    
    # Forzar la recarga de enums limpiando el cache de SQLAlchemy
    from sqlalchemy import inspect
    inspector = inspect(engine)
    # Limpiar el cache forzando una nueva conexión
    inspector.get_table_names()
    
    # Limpiar completamente el cache de tipos de enum
    from sqlalchemy import event
    from sqlalchemy.engine import Engine
    
    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        # Forzar la recarga de metadatos
        if hasattr(dbapi_connection, 'execute'):
            dbapi_connection.execute("SELECT 1")
    
    # Forzar la recarga de metadatos
    from sqlalchemy import MetaData
    metadata = MetaData()
    metadata.reflect(bind=engine)
    
    # Limpiar el cache de tipos de enum específicamente
    from sqlalchemy import types
    if hasattr(types, '_type_map'):
        types._type_map.clear()
    
    print("Cache de SQLAlchemy limpiado.")
    
    create_db_tables() # Call the function to create database tables
    print("Database tables created.")

# Configure CORS middleware
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Root endpoint for testing the API
@app.get("/")
async def root():
    return {"message": "Welcome to SOUP Emprendimientos API!"}

# Include routers for authentication, user profile, businesses, products, public, and now insumos
app.include_router(auth_router.router, prefix="/users", tags=["Authentication"])
app.include_router(user_router.router, prefix="/profile", tags=["User Profile"])
app.include_router(business_router.router, prefix="/businesses", tags=["Businesses"])
app.include_router(product_router.router, prefix="/products", tags=["Products & Services"])
app.include_router(public_router.router, prefix="/public", tags=["Public Listing & Search"])
# CAMBIO AQUI: Eliminar el prefijo duplicado para insumo_router
app.include_router(insumo_router.router, tags=["Insumos"])
app.include_router(public_ai_router.router, tags=["AI Recomendaciones"])
app.include_router(plugin_router.router, tags=["Plugins"])
app.include_router(venta_router.router, tags=["Ventas & POS"])
app.include_router(niam_router.router, tags=["Panadería Ñiam"])
