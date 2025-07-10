from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from typing import List, Optional, Union
from app.schemas import ProductoResponse, NegocioResponse
from app.models import Producto, Negocio
from app.database import SessionLocal
from sqlalchemy.orm import Session
import requests
import os
import uuid

router = APIRouter()

# Dependencia para obtener la sesión de base de datos

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Esquema de entrada para la consulta AI
class AIRecommendRequest(BaseModel):
    query: str

# Esquema de salida (puede ser una lista de productos, negocios o ambos)
class AIRecommendResponse(BaseModel):
    productos: Optional[List[ProductoResponse]] = None
    negocios: Optional[List[NegocioResponse]] = None

# Utilidad para llamar a Gemini API (gemini-2.0-flash)
def call_gemini_api(query: str, productos_info: list) -> dict:
    import json
    apiKey = os.environ.get("GEMINI_API_KEY", "")
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    headers = {"Content-Type": "application/json"}
    productos_json = json.dumps(productos_info, ensure_ascii=False)
    prompt = (
        "Eres un asistente de recomendaciones para una app de productos y negocios. "
        "Solo puedes recomendar productos de la siguiente lista (usa exactamente los IDs y nombres que aparecen):\n"
        f"{productos_json}\n"
        "Responde SOLO en JSON con el siguiente formato: "
        '{"producto_preferencial": {"id": <id>, "nombre": <nombre>, "tipo": <tipo>, "precio": <precio>, "negocio_id": <negocio_id>, "negocio_nombre": <negocio_nombre>}, '
        '"otras_recomendaciones": [{"id": <id>, "nombre": <nombre>, "tipo": <tipo>, "precio": <precio>, "negocio_id": <negocio_id>, "negocio_nombre": <negocio_nombre>}]} '
        "No incluyas explicaciones ni texto fuera del JSON. "
        "La consulta del usuario es: " + query
    )
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    print("Payload enviado a Gemini:", payload)
    params = {"key": apiKey}
    try:
        response = requests.post(url, headers=headers, params=params, json=payload, timeout=15)
        response.raise_for_status()
        data = response.json()
        if "candidates" in data and data["candidates"]:
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            # Limpiar bloque Markdown si existe
            text = text.strip()
            if text.startswith("```"):
                lines = text.splitlines()
                if lines[0].strip().startswith("```"):
                    lines = lines[1:]
                if lines and lines[-1].strip().startswith("```"):
                    lines = lines[:-1]
                text = "\n".join(lines).strip()
            import json as _json
            try:
                return _json.loads(text)
            except Exception as e:
                print("ERROR AL PARSEAR JSON DE GEMINI:", text)
                raise HTTPException(status_code=500, detail="La IA no devolvió un JSON válido.")
        else:
            raise ValueError("Respuesta inesperada de Gemini")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al consultar Gemini: {str(e)}")

@router.post("/public/ai/recommend", response_model=dict)
def recommend_ai(
    req: AIRecommendRequest,
    db: Session = Depends(get_db)
):
    # Extraer productos públicos de la base de datos
    productos = db.query(Producto).all()
    productos_info = [
        {
            "id": str(p.id),
            "nombre": p.nombre,
            "tipo": p.tipo_producto,
            "precio": p.precio,
            "negocio_id": str(p.negocio_id),
            "negocio_nombre": p.negocio.nombre if p.negocio else ""
        }
        for p in productos
    ]
    try:
        params = call_gemini_api(req.query, productos_info)
    except Exception as e:
        print("ERROR EN LLAMADA A GEMINI:", repr(e))
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

    # Buscar producto preferencial y otras recomendaciones en la BD
    producto_pref = None
    otras_recs = []
    if "producto_preferencial" in params:
        prod_id = params["producto_preferencial"].get("id")
        producto_pref = None
        if prod_id:
            try:
                prod_uuid = uuid.UUID(str(prod_id))
                producto_pref = db.query(Producto).filter_by(id=prod_uuid).first()
            except (ValueError, TypeError):
                nombre = params["producto_preferencial"].get("nombre")
                if nombre:
                    producto_pref = db.query(Producto).filter_by(nombre=nombre).first()
    if "otras_recomendaciones" in params:
        for rec in params["otras_recomendaciones"]:
            prod_id = rec.get("id")
            prod = None
            if prod_id:
                try:
                    prod_uuid = uuid.UUID(str(prod_id))
                    prod = db.query(Producto).filter_by(id=prod_uuid).first()
                except (ValueError, TypeError):
                    nombre = rec.get("nombre")
                    if nombre:
                        prod = db.query(Producto).filter_by(nombre=nombre).first()
            if prod:
                otras_recs.append(prod)
    # Serializar
    from app.schemas import ProductoResponse
    resp = {
        "producto_preferencial": ProductoResponse.model_validate(producto_pref, from_attributes=True) if producto_pref else None,
        "otras_recomendaciones": [ProductoResponse.model_validate(p, from_attributes=True) for p in otras_recs]
    }
    return resp 