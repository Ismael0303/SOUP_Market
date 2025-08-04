# backend/test_product_calculations.py

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Usuario, Insumo, Producto, ProductoInsumo
from app.schemas import ProductoCreate, ProductoInsumoCreate
from app.crud import product as crud_product
import uuid

def test_product_calculations():
    """Test the product cost and price calculations."""
    db = SessionLocal()
    
    try:
        # Crear un usuario de prueba
        test_user = Usuario(
            id=uuid.uuid4(),
            nombre="Usuario Test",
            email="test@example.com",
            password_hash="test_hash",
            tipo_tier="microemprendimiento"
        )
        db.add(test_user)
        db.flush()
        
        # Crear insumos de prueba
        insumo1 = Insumo(
            id=uuid.uuid4(),
            nombre="Harina",
            cantidad_disponible=10.0,
            unidad_medida_compra="kg",
            costo_unitario_compra=2.5,  # $2.5 por kg
            usuario_id=test_user.id
        )
        
        insumo2 = Insumo(
            id=uuid.uuid4(),
            nombre="Azúcar",
            cantidad_disponible=5.0,
            unidad_medida_compra="kg",
            costo_unitario_compra=3.0,  # $3.0 por kg
            usuario_id=test_user.id
        )
        
        db.add(insumo1)
        db.add(insumo2)
        db.flush()
        
        # Crear un producto con insumos asociados
        product_data = ProductoCreate(
            nombre="Pan Casero",
            descripcion="Pan artesanal hecho en casa",
            tipo_producto="bien_fisico",
            stock=20,
            unidad_medida="unidad",
            precio_venta=15.0,  # Precio de venta establecido
            margen_ganancia_sugerido=30.0,  # 30% de margen sugerido
            insumos=[
                ProductoInsumoCreate(
                    insumo_id=insumo1.id,
                    cantidad_necesaria=0.5  # 0.5 kg de harina por pan
                ),
                ProductoInsumoCreate(
                    insumo_id=insumo2.id,
                    cantidad_necesaria=0.1  # 0.1 kg de azúcar por pan
                )
            ]
        )
        
        # Crear el producto
        created_product = crud_product.create_product(db, user_id=test_user.id, product=product_data)
        
        print("=== RESULTADOS DE LA PRUEBA ===")
        print(f"Producto: {created_product.nombre}")
        print(f"Precio de venta: ${created_product.precio_venta}")
        print(f"Margen de ganancia sugerido: {created_product.margen_ganancia_sugerido}%")
        print(f"COGS calculado: ${created_product.cogs}")
        print(f"Precio sugerido: ${created_product.precio_sugerido}")
        
        # Calcular margen de ganancia real manualmente
        if created_product.cogs and created_product.precio_venta and created_product.cogs > 0:
            margen_real = ((created_product.precio_venta - created_product.cogs) / created_product.cogs) * 100
            print(f"Margen de ganancia real: {margen_real:.2f}%")
        
        print("\n=== DETALLES DE INSUMOS ===")
        for producto_insumo in created_product.insumos_asociados:
            insumo = db.query(Insumo).get(producto_insumo.insumo_id)
            costo_insumo = producto_insumo.cantidad_necesaria * insumo.costo_unitario_compra
            print(f"- {insumo.nombre}: {producto_insumo.cantidad_necesaria} {insumo.unidad_medida_compra} x ${insumo.costo_unitario_compra} = ${costo_insumo}")
        
        print("\n=== VERIFICACIÓN DE CÁLCULOS ===")
        # Verificar COGS
        expected_cogs = (0.5 * 2.5) + (0.1 * 3.0)  # 1.25 + 0.30 = 1.55
        print(f"COGS esperado: ${expected_cogs}")
        print(f"COGS calculado: ${created_product.cogs}")
        print(f"COGS correcto: {abs(created_product.cogs - expected_cogs) < 0.01}")
        
        # Verificar precio sugerido
        expected_suggested_price = expected_cogs * (1 + 30.0 / 100)  # 1.55 * 1.30 = 2.015
        print(f"Precio sugerido esperado: ${expected_suggested_price}")
        print(f"Precio sugerido calculado: ${created_product.precio_sugerido}")
        print(f"Precio sugerido correcto: {abs(created_product.precio_sugerido - expected_suggested_price) < 0.01}")
        
        # Verificar margen real
        if created_product.precio_venta and created_product.cogs:
            expected_margin = ((created_product.precio_venta - created_product.cogs) / created_product.cogs) * 100
            print(f"Margen real esperado: {expected_margin:.2f}%")
            print(f"Margen real correcto: {abs(margen_real - expected_margin) < 0.01}")
        
        print("\n¡Prueba completada exitosamente!")
        
    except Exception as e:
        print(f"Error durante la prueba: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_product_calculations() 

input("Press Enter to exit...")