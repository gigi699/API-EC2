from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(
    title="API de Productos y Pedidos",
    description="API RESTful desarrollada con FastAPI para la actividad en AWS EC2",
    version="1.0.0"
)

# ==========================================
# MODELOS PYDANTIC
# ==========================================

class ProductoCreate(BaseModel):
    nombre: str
    precio: float
    stock: int

class Producto(ProductoCreate):
    id: int

class PedidoCreate(BaseModel):
    producto_id: int
    cantidad: int
    cliente: str

class Pedido(PedidoCreate):
    id: int

# ==========================================
# BASE DE DATOS EN MEMORIA (SIMULADA)
# ==========================================

db_productos: List[Producto] = [
    Producto(id=1, nombre="Laptop Pro", precio=1250.00, stock=10),
    Producto(id=2, nombre="Mouse Inalámbrico", precio=25.50, stock=50)
]

db_pedidos: List[Pedido] = [
    Pedido(id=1, producto_id=1, cantidad=1, cliente="Ana Gómez")
]

# ==========================================
# ENDPOINTS: PRODUCTOS
# ==========================================

@app.get("/productos/", response_model=List[Producto], tags=["Productos"])
def obtener_productos():
    return db_productos

@app.post("/productos/", response_model=Producto, status_code=201, tags=["Productos"])
def crear_producto(producto: ProductoCreate):
    nuevo_id = max([p.id for p in db_productos], default=0) + 1
    nuevo_producto = Producto(id=nuevo_id, **producto.model_dump())
    db_productos.append(nuevo_producto)
    return nuevo_producto

@app.get("/productos/{producto_id}", response_model=Producto, tags=["Productos"])
def obtener_producto(producto_id: int):
    for producto in db_productos:
        if producto.id == producto_id:
            return producto
    raise HTTPException(status_code=404, detail="Producto no encontrado")

@app.put("/productos/{producto_id}", response_model=Producto, tags=["Productos"])
def actualizar_producto(producto_id: int, producto_actualizado: ProductoCreate):
    for index, producto in enumerate(db_productos):
        if producto.id == producto_id:
            producto_modificado = Producto(id=producto_id, **producto_actualizado.model_dump())
            db_productos[index] = producto_modificado
            return producto_modificado
    raise HTTPException(status_code=404, detail="Producto no encontrado")

@app.delete("/productos/{producto_id}", tags=["Productos"])
def eliminar_producto(producto_id: int):
    for index, producto in enumerate(db_productos):
        if producto.id == producto_id:
            db_productos.pop(index)
            return {"mensaje": f"Producto con ID {producto_id} eliminado exitosamente"}
    raise HTTPException(status_code=404, detail="Producto no encontrado")

# ==========================================
# ENDPOINTS: PEDIDOS
# ==========================================

@app.get("/pedidos/", response_model=List[Pedido], tags=["Pedidos"])
def obtener_pedidos():
    return db_pedidos

@app.post("/pedidos/", response_model=Pedido, status_code=201, tags=["Pedidos"])
def crear_pedido(pedido: PedidoCreate):
    # Validar que el producto exista antes de hacer el pedido
    producto_existe = any(p.id == pedido.producto_id for p in db_productos)
    if not producto_existe:
        raise HTTPException(status_code=400, detail="El producto asociado no existe")
    
    nuevo_id = max([p.id for p in db_pedidos], default=0) + 1
    nuevo_pedido = Pedido(id=nuevo_id, **pedido.model_dump())
    db_pedidos.append(nuevo_pedido)
    return nuevo_pedido

@app.get("/pedidos/{pedido_id}", response_model=Pedido, tags=["Pedidos"])
def obtener_pedido(pedido_id: int):
    for pedido in db_pedidos:
        if pedido.id == pedido_id:
            return pedido
    raise HTTPException(status_code=404, detail="Pedido no encontrado")

@app.delete("/pedidos/{pedido_id}", tags=["Pedidos"])
def eliminar_pedido(pedido_id: int):
    for index, pedido in enumerate(db_pedidos):
        if pedido.id == pedido_id:
            db_pedidos.pop(index)
            return {"mensaje": f"Pedido con ID {pedido_id} eliminado exitosamente"}
    raise HTTPException(status_code=404, detail="Pedido no encontrado")