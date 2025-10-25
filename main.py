from fastapi import FastAPI
from app.router.router import router

app = FastAPI(
    title="Brick Builder Catalogue", 
    description="Find which brick sets you can build with your collection"
)

# Include API routes
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)