from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.supabase_client import get_supabase

router = APIRouter()

class SignupSchema(BaseModel):
    email: str
    password: str
    user_data: dict = {}

class UserSignup(BaseModel):
    email: str
    password: str
    user_data: dict

class UserLogin(BaseModel):
    email: str
    password: str


@router.post("/auth/signup")
async def sign_up(data: SignupSchema):
    try:
        supabase = get_supabase()
        result = supabase.auth.sign_up({
            "email": data.email,
            "password": data.password
        })
        
        error = getattr(result, "error", None)
        if error:
            raise HTTPException(status_code=400, detail=str(error))
        
        return {"message": "Usuario creado correctamente", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.post("/login")
async def sign_in(user: UserLogin):
    try:
        supabase = get_supabase()
        print("LOGIN ATTEMPT:", user.email)

        # Forma más directa de manejar la autenticación
        response = supabase.auth.sign_in_with_password({
            "email": user.email,
            "password": user.password
        })

        print("LOGIN RESPONSE:", response)

        # Manejo de errores mejorado
        if hasattr(response, 'error') and response.error:
            raise HTTPException(status_code=401, detail=response.error.message)

        # Obtener datos de la sesión
        session = response.session
        user_data = response.user

        return {
            "message": "Login exitoso",
            "session": {
                "access_token": session.access_token,
                "refresh_token": session.refresh_token,
                "expires_at": session.expires_at
            },
            "user": {
                "id": user_data.id,
                "email": user_data.email,
                # Agrega otros campos que necesites
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        print("ERROR DETAIL:", str(e))  # Para depuración
        raise HTTPException(status_code=500, detail="Error durante el login")

@router.post("/signout")
def sign_out():  # Requiere token válido si se implementa sesión
    supabase = get_supabase()
    result = supabase.auth.sign_out()
    if result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"]["message"])
    return {"message": "Sesión cerrada"}
