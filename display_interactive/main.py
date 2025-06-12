import uvicorn
from fastapi import FastAPI

from display_interactive.routers import import_csv, export

app = FastAPI()

# Add router
app.include_router(import_csv.router)
app.include_router(export.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
