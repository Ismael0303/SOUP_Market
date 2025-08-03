# backend/app/routers/plugin_router.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import get_db
from app.dependencies import get_current_user
from app.models import Usuario
from app.crud.user import activate_plugin, deactivate_plugin, get_user_plugins
from app.schemas import UsuarioResponse

router = APIRouter(prefix="/plugins", tags=["plugins"])

# Lista de plugins disponibles
AVAILABLE_PLUGINS = {
    "panaderia": {
        "name": "Panadería",
        "description": "Sistema POS y gestión de inventario para panaderías",
        "version": "1.0.0",
        "category": "business",
        "features": ["POS", "Inventario", "Análisis Financiero"]
    },
    "discografica": {
        "name": "Discográfica",
        "description": "Gestión de artistas, álbumes y ventas de música",
        "version": "1.0.0",
        "category": "business",
        "features": ["Gestión de Artistas", "Catálogo", "Ventas"]
    },
    "freelancer": {
        "name": "Freelancer",
        "description": "Gestión de proyectos y clientes para freelancers",
        "version": "1.0.0",
        "category": "business",
        "features": ["Proyectos", "Clientes", "Facturación"]
    }
}

@router.get("/available")
def get_available_plugins():
    """Obtiene la lista de plugins disponibles"""
    return {
        "plugins": AVAILABLE_PLUGINS,
        "total": len(AVAILABLE_PLUGINS)
    }

@router.get("/my-plugins")
def get_my_plugins(
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtiene los plugins activos del usuario actual"""
    plugins = get_user_plugins(db, current_user.id)
    
    # Obtener información detallada de los plugins activos
    active_plugins_info = {}
    for plugin_name in plugins:
        if plugin_name in AVAILABLE_PLUGINS:
            active_plugins_info[plugin_name] = AVAILABLE_PLUGINS[plugin_name]
    
    return {
        "active_plugins": plugins,
        "plugins_info": active_plugins_info,
        "total_active": len(plugins)
    }

@router.post("/activate/{plugin_name}")
def activate_user_plugin(
    plugin_name: str,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Activa un plugin para el usuario actual"""
    if plugin_name not in AVAILABLE_PLUGINS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Plugin '{plugin_name}' no está disponible"
        )
    
    updated_user = activate_plugin(db, current_user.id, plugin_name)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    return {
        "message": f"Plugin '{plugin_name}' activado exitosamente",
        "user": UsuarioResponse.from_orm(updated_user)
    }

@router.post("/deactivate/{plugin_name}")
def deactivate_user_plugin(
    plugin_name: str,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Desactiva un plugin para el usuario actual"""
    updated_user = deactivate_plugin(db, current_user.id, plugin_name)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    return {
        "message": f"Plugin '{plugin_name}' desactivado exitosamente",
        "user": UsuarioResponse.from_orm(updated_user)
    }

@router.get("/status")
def get_plugin_status(
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtiene el estado completo de plugins del usuario"""
    active_plugins = get_user_plugins(db, current_user.id)
    
    # Crear estado detallado
    status_info = {}
    for plugin_name, plugin_info in AVAILABLE_PLUGINS.items():
        status_info[plugin_name] = {
            **plugin_info,
            "active": plugin_name in active_plugins
        }
    
    return {
        "user_id": current_user.id,
        "active_plugins": active_plugins,
        "plugins_status": status_info,
        "total_available": len(AVAILABLE_PLUGINS),
        "total_active": len(active_plugins)
    } 