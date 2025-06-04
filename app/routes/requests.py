# app/routes/products.py
from fastapi import APIRouter, HTTPException
from app.supabase_client import supabase
from app.models.requests import NewRequest, RequestStatusUpdate
from uuid import UUID
from fastapi import Path, Query
from typing import List

router = APIRouter()

@router.post("")
def create_request(new_request: NewRequest):
    try:
        data = new_request.dict()
        data["product_id"] = str(data["product_id"])
        data["user_id"] = str(data["user_id"])
        if data.get("product_item_id") is not None:
            data["product_item_id"] = str(data["product_item_id"])
        data["status"] = "pending"

        # Verificar si el producto es individual
        product_response = supabase.table("products").select("is_individual").eq("id", data["product_id"]).single().execute()
        if not product_response.data:
            raise HTTPException(status_code=404, detail="Producto no encontrado")

        is_individual = product_response.data["is_individual"]

        if is_individual:
            if not new_request.product_item_id:
                raise HTTPException(status_code=400, detail="Debes proporcionar un item del producto individual")

            # Obtener el product_item
            item_response = supabase.table("product_items").select("product_id").eq("id", data["product_item_id"]).single().execute()
            if not item_response.data:
                raise HTTPException(status_code=404, detail="El item del producto no existe")

            if item_response.data["product_id"] != data["product_id"]:
                raise HTTPException(status_code=400, detail="Este item no corresponde al producto seleccionado")

        # Insertar la solicitud
        response = supabase.table("requests").insert(data).execute()
        return {"message": "Solicitud creada correctamente", "request": response.data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")
    
@router.put("/{request_id}/status")
def update_request_status(request_id: str = Path(...), status_update: RequestStatusUpdate = ...):
    allowed_status = {'pending', 'approved', 'rejected'}
    if status_update.status not in allowed_status:
        raise HTTPException(status_code=400, detail="Estado inválido")

    try:
        response = supabase.table("requests").update({"status": status_update.status}).eq("id", request_id).execute()

        if not response.data:
            raise HTTPException(status_code=404, detail="Solicitud no encontrada")

        return {"message": "Estado de solicitud actualizado correctamente", "request": response.data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

@router.get("/filter")
def get_requests_filtered(
    user_id: str = Query(None),
    product_id: str = Query(None),
    status: str = Query(None)
):
    try:
        query = supabase.table("requests").select("*")
        if user_id:
            query = query.eq("user_id", user_id)
        if product_id:
            query = query.eq("product_id", product_id)
        if status:
            query = query.eq("status", status)
        response = query.execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

@router.get("")
def get_all_requests():
    try:
        response = supabase.table("requests").select("*").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

@router.delete("/{request_id}")
def delete_request(request_id: str = Path(..., description="ID de la solicitud a eliminar")):
    try:
        response = supabase.table("requests") \
            .delete() \
            .eq("id", request_id) \
            .eq("status", "pending") \
            .execute()

        if response.count == 0:
            raise HTTPException(status_code=404, detail="Solicitud no encontrada o no está en estado 'pending'")

        return {"message": "Solicitud eliminada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")
