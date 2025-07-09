# app/routes/products.py
from fastapi import APIRouter, HTTPException
from app.supabase_client import get_supabase
from app.models.product import Product, NewProduct, ProductUpdate
from fastapi import Path
from typing import List
import logging

router = APIRouter()

@router.get("")
def get_all_products():
    try:
        # Get a fresh client instance
        supabase = get_supabase()
        response = supabase.table("products").select("*").execute()
        
        # Check if the response has data
        if hasattr(response, 'data'):
            return {"data": response.data, "count": len(response.data)}
        else:
            return {"data": [], "count": 0}
    
    except Exception as e:
        logging.error(f"Error fetching products: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching products: {str(e)}"
        )
    
@router.post("")
def create_product(product: NewProduct):
    try:
        supabase = get_supabase()
        response = supabase.table("products").insert(product.dict()).execute()
        
        if hasattr(response, 'data') and response.data:
            return {"data": response.data[0], "message": "Product created successfully"}
        else:
            raise HTTPException(status_code=500, detail="Product creation failed")

    except Exception as e:
        logging.error(f"Error creating product: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creating product: {str(e)}")
    

@router.put("/{product_id}")
def update_product(
    product_id: str = Path(..., description="ID del producto a actualizar"),
    product: ProductUpdate = ...
):
    data_to_update = product.dict(exclude_unset=True)
    
    if not data_to_update:
        raise HTTPException(status_code=400, detail="No se enviaron campos para actualizar")
    
    try:
        supabase = get_supabase()
        response = supabase.table("products").update(data_to_update).eq("id", product_id).execute()
        
        if hasattr(response, 'data') and response.data:
            return {"message": "Producto actualizado correctamente", "product": response.data[0]}
        else:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    except Exception as e:
        logging.error(f"Error updating product: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating product: {str(e)}")

@router.delete("/{product_id}")
def delete_product(product_id: str = Path(..., description="ID del producto a eliminar")):
    try:
        supabase = get_supabase()
        response = supabase.table("products").delete().eq("id", product_id).execute()

        if hasattr(response, 'data') and response.data:
            return {"message": "Producto eliminado correctamente"}
        else:
            raise HTTPException(status_code=404, detail="Producto no encontrado")

    except Exception as e:
        logging.error(f"Error deleting product: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error deleting product: {str(e)}")
