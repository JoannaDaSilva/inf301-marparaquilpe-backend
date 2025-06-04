# app/routes/products.py
from fastapi import APIRouter, HTTPException
from app.supabase_client import supabase
from app.models.product import Product, NewProduct, ProductUpdate
from fastapi import Path
from typing import List

router = APIRouter()

@router.get("")
def get_all_products():
    try:
        response = supabase.table("products").select("*").execute()
        return response
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error inesperado: {str(e)}"
        )
    
@router.post("")
def create_product(product: NewProduct):
    try:
        response = supabase.table("products").insert(product.dict()).execute()
        return response.data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")
    

@router.put("/{product_id}")
def update_product(
    product_id: str = Path(..., description="ID del producto a actualizar"),
    product: ProductUpdate = ...
):
    data_to_update = product.dict(exclude_unset=True)
    
    if not data_to_update:
        raise HTTPException(status_code=400, detail="No se enviaron campos para actualizar")
    
    try:
        response = supabase.table("products").update(data_to_update).eq("id", product_id).execute()
        
        return {"message": "Producto actualizado correctamente", "product": response.data}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

@router.delete("/{product_id}")
def delete_product(product_id: str = Path(..., description="ID del producto a eliminar")):
    try:
        response = supabase.table("products").delete().eq("id", product_id).execute()

        if response.count == 0:
            raise HTTPException(status_code=404, detail="Producto no encontrado")

        return {"message": "Producto eliminado correctamente"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")
