from app.supabase_client import supabase
from fastapi import HTTPException

def get_user(access_token: str):
    res = supabase.auth.get_user(access_token)
    if res.get("error"):
        raise HTTPException(status_code=401, detail="Token inválido")
    return res["data"]["user"]

def is_admin(user):
    response = supabase.from_("users").select("role").eq("id", user["id"]).single().execute()
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return response.data["role"] == "admin"

def update_user_role(user_id: str, role: str):
    # Tabla personalizada
    table_update = supabase.from_("users").update({"role": role}).eq("id", user_id).execute()
    if table_update.error:
        raise HTTPException(status_code=400, detail=table_update.error.message)

    # Metadatos auth
    auth_update = supabase.auth.admin.update_user_by_id(user_id, {
        "app_metadata": {"role": role}
    })
    if auth_update.get("error"):
        raise HTTPException(status_code=400, detail=auth_update["error"]["message"])

    return {"success": True}
