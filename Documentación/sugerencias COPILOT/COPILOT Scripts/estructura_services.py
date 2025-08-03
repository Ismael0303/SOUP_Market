# Script: Estructura de servicios para lógica de negocio

"""
Ejemplo de cómo crear una carpeta 'services' y separar la lógica de negocio de los routers.
Coloca este ejemplo en backend/app/services/user_service.py y llama a las funciones desde tus routers.
"""

# backend/app/services/user_service.py
from app.crud import user as user_crud

def create_user_service(user_data):
    # Aquí puedes agregar lógica adicional, validaciones, etc.
    return user_crud.create_user(user_data)

# En tu router:
# from app.services.user_service import create_user_service
# ...
# user = create_user_service(user_data)
