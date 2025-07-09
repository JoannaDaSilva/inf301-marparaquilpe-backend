# app/routes/loans.py
from fastapi import APIRouter, HTTPException, Query
from app.supabase_client import get_supabase
from app.models.loans import LoanCreate, LoanUpdate
from datetime import date, timedelta
from typing import Optional

router = APIRouter()

@router.post("")
def create_loan(loan: LoanCreate):
    try:
        supabase = get_supabase()
        request_id = str(loan.request_id)
        due_date = loan.due_date or (date.today() + timedelta(days=7))

        # Verificar que la solicitud exista y esté aprobada
        req = supabase.table("requests").select("*").eq("id", request_id).single().execute()
        if not req.data:
            raise HTTPException(status_code=404, detail="Solicitud no encontrada")
        
        request_data = req.data
        if request_data["status"] != "approved":
            raise HTTPException(status_code=400, detail="La solicitud debe estar 'approved'")

        # Extraer datos relacionados
        user_id = request_data["user_id"]
        product_id = request_data["product_id"]
        is_individual = request_data.get("is_individual", False)

        loan_data = {
            "request_id": request_id,
            "user_id": user_id,
            "product_id": product_id,
            "start_date": date.today().isoformat(),
            "due_date": due_date.isoformat(),
            "status": "active"
        }

        response = supabase.table("loans").insert(loan_data).execute()
        if response.error or not response.data:
            raise HTTPException(status_code=400, detail=f"No se pudo crear el préstamo: {response.error.message if response.error else 'sin datos'}")

        loan_created = response.data[0]
        loan_id = loan_created["id"]

        # Si es individual, insertar loan_items
        if is_individual:
            item_query = supabase.table("product_items").select("id").eq("request_id", request_id).execute()
            item_ids = [item["id"] for item in item_query.data] if item_query.data else []

            if not item_ids:
                raise HTTPException(status_code=400, detail="No hay ítems individuales asociados a esta solicitud")

            loan_items_data = [{"loan_id": loan_id, "product_item_id": pid} for pid in item_ids]
            supabase.table("loan_items").insert(loan_items_data).execute()

        return {"message": "Préstamo creado correctamente", "loan": loan_created}

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

@router.get("")
def get_all_loans():
    try:
        supabase = get_supabase()
        response = supabase.table("loans").select("*").execute()

        if not response.data:
            raise HTTPException(status_code=500, detail=f"Error al obtener los préstamos: {response.error.message}")
        return response.data

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")
    

@router.get("/filter")
def filter_loans(
    user_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    product_id: Optional[str] = Query(None),
    request_id: Optional[str] = Query(None),
):
    try:
        supabase = get_supabase()
        query = supabase.table("loans").select("*")

        if user_id:
            query = query.eq("user_id", user_id)
        if status:
            query = query.eq("status", status)
        if product_id:
            query = query.eq("product_id", product_id)
        if request_id:
            query = query.eq("request_id", request_id)

        response = query.execute()

        if not response.data:
            raise HTTPException(status_code=500, detail=f"Error al filtrar préstamos: {response.error.message}")
        return response.data

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")
    

@router.patch("/{loan_id}")
def update_loan(loan_id: str, update_data: LoanUpdate):
    try:
        supabase = get_supabase()
        if not update_data.due_date and not update_data.status:
            raise HTTPException(status_code=400, detail="Debes enviar al menos 'due_date' o 'status' para actualizar")

        payload = {}
        if update_data.due_date:
            payload["due_date"] = update_data.due_date.isoformat()
        if update_data.status:
            payload["status"] = update_data.status

        response = supabase.table("loans").update(payload).eq("id", loan_id).execute()

        if not response.data:
            raise HTTPException(status_code=404, detail="Préstamo no encontrado o no se pudo actualizar")

        return {"message": "Préstamo actualizado correctamente", "loan": response.data[0]}

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")


@router.delete("/{loan_id}")
def delete_loan(loan_id: str):
    try:
        supabase = get_supabase()
        # Verificar que el préstamo existe
        loan_check = supabase.table("loans").select("*").eq("id", loan_id).single().execute()
        if not loan_check.data:
            raise HTTPException(status_code=404, detail="Préstamo no encontrado")

        loan_data = loan_check.data

        # Solo permitir eliminación si el préstamo NO está activo
        if loan_data["status"] == "active":
            raise HTTPException(status_code=400, detail="No se pueden eliminar préstamos con estado 'active'")

        # Eliminar loan_items asociados si existen
        loan_items = supabase.table("loan_items").select("id").eq("loan_id", loan_id).execute()
        if loan_items.data:
            loan_item_ids = [item["id"] for item in loan_items.data]
            supabase.table("loan_items").delete().in_("id", loan_item_ids).execute()

        # Eliminar el préstamo
        response = supabase.table("loans").delete().eq("id", loan_id).execute()
        if not response.data:
            raise HTTPException(status_code=400, detail=f"No se pudo eliminar el préstamo: {response.error.message}")

        return {"message": f"Préstamo {loan_id} eliminado correctamente"}

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")