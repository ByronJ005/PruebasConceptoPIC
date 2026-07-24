from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from src.core.config import settings
from src.api.auth_router import router as auth_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Modulo de Autenticacion para el sistema web de reserva de boletos de cooperativas de transporte.",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Standardized Error Handling
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Standardize error message formatting to avoid leakage and provide clean messages
    errors = []
    for error in exc.errors():
        field = ".".join(str(p) for p in error["loc"][1:])
        errors.append({
            "field": field,
            "message": error["msg"]
        })
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "Validation Error", "errors": errors}
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # Avoid exposing internal stack traces in production (constitution requirement)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal server error occurred."}
    )

# Include Auth Router
app.include_router(auth_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to transport cooperative tickets API"}
