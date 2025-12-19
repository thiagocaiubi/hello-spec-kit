from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def health() -> dict[str, str]:
    """Health check endpoint for Kubernetes probes.
    
    Returns a simple status response to indicate the application is running
    and ready to handle requests. Used by Kubernetes readiness and liveness probes.
    
    Returns:
        dict: JSON response with status "ok"
    """
    return {"status": "ok"}


@app.get("/")
async def read_root():
    return {"message": "FastAPI is running!"}
