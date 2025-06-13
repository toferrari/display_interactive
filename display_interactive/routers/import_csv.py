import logging
from fastapi import HTTPException
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from display_interactive.backend.sqlite import get_db
from display_interactive.schemas.import_csv import ImportCSV
from display_interactive.services.import_csv import import_csv

log = logging.getLogger(__name__)

router = APIRouter(tags=["csv"], prefix="")


@router.post("/import-csv", response_model=None)
async def import_csv_files(
        request: ImportCSV,
        db: Session = Depends(get_db)
):
    """
    Import data from CSV files into the database.
    """
    try:
        await import_csv(request, db)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"An error occurred while importing CSV files: {exc}")
