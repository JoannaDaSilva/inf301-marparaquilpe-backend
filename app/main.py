from fastapi import FastAPI
from app.routes.products import router as products_router
from app.routes.loans import router as loans_router

app = FastAPI(title="MarParaQuilpe Backend", version="1.0.0")

# Health check endpoint
@app.get("/")
def health_check():
    return {"message": "MarParaQuilpe Backend is running!", "status": "healthy"}

# Include routers
app.include_router(products_router, prefix="/products")
app.include_router(loans_router, prefix="/loans")

# For Vercel deployment
handler = app