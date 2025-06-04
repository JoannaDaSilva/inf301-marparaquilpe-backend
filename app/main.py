from fastapi import FastAPI
from app.auth.routes import router as auth_router
from app.routes.products import router as products_router
from app.routes.requests import router as requests_router
from app.routes.loans import router as loans_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth")
app.include_router(products_router, prefix="/products")
app.include_router(requests_router, prefix="/requests")
app.include_router(loans_router, prefix="/loans")