from fastapi import FastAPI

app = FastAPI(
    title="IronPath API",
    description="AI-powered gym progression platform",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Welcome to IronPath 🚀"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }