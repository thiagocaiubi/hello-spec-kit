from fastapi import FastAPI

from models.schemas import HealthResponse

app = FastAPI()


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """Health check endpoint for Kubernetes probes.
    
    Returns a simple status response to indicate the application is running
    and ready to handle requests. Used by Kubernetes readiness and liveness probes.
    
    Returns:
        HealthResponse: Pydantic model with status "ok"
    """
    return HealthResponse(status="ok")


@app.get("/")
async def read_root():
    return {"message": "FastAPI is running!"}
