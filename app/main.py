from fastapi import FastAPI
from app.routes.products import router as products_router

app = FastAPI(title="MarParaQuilpe Backend", version="1.0.0")

# Health check endpoint
@app.get("/")
def health_check():
    return {"message": "MarParaQuilpe Backend is running!", "status": "healthy"}

# Include routers
app.include_router(products_router, prefix="/products")

# For Vercel deployment
handler = app