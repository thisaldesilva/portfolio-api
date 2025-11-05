"""Main FastAPI application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app

from app.config import get_settings
from app.api import customers, stocks, portfolio

settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title="Customer Portfolio Management API",
    description="Production-grade REST API for managing customer portfolios with real-time stock data",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(customers.router, prefix="/api/v1")
app.include_router(stocks.router, prefix="/api/v1")
app.include_router(portfolio.router, prefix="/api/v1")

# Metrics endpoint (Prometheus)
if settings.enable_metrics:
    metrics_app = make_asgi_app()
    app.mount("/metrics", metrics_app)


@app.get("/", tags=["health"])
def root():
    """Root endpoint."""
    return {
        "name": "Customer Portfolio Management API",
        "version": "1.0.0",
        "status": "running",
        "environment": settings.environment,
    }


@app.get("/health", tags=["health"])
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.on_event("startup")
async def startup_event():
    """Actions to perform on application startup."""
    print(f"Starting application in {settings.environment} mode...")
    print(
        f"API documentation available at: http://{settings.app_host}:{settings.app_port}/docs"
    )


@app.on_event("shutdown")
async def shutdown_event():
    """Actions to perform on application shutdown."""
    print("Shutting down application...")
