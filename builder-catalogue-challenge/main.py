from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.router.router import router

# Create FastAPI app with basic metadata
app = FastAPI(
    title="Brick Builder Catalogue", 
    description="Find which brick sets you can build with your collection"
)

# Mount static files for CSS and assets
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include all routes (frontend + API)
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    # Start development server
    uvicorn.run(app, host="0.0.0.0", port=8000)