from fastapi import FastAPI
from backend.api.health import router as health_router
from backend.api.solve import router as solve_router

app = FastAPI(
    title="Ink2Math API",
    description="Backend for Handwritten Mathematical Expression Recognition",
    version="1.0.0"
)

app.include_router(health_router)
app.include_router(solve_router)
