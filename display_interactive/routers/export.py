import logging
from fastapi import HTTPException
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, BackgroundTasks
from starlette.responses import JSONResponse

from display_interactive.backend.sqlite import get_db
from display_interactive.services.export import export_database, update_state_after_export, send_to_external_api


log = logging.getLogger(__name__)

router = APIRouter(tags=["export"], prefix="")


@router.post("/send-customers")
async def export_data(
        background_tasks: BackgroundTasks,
        db: Session = Depends(get_db)
):
    """
    Export data from the database and send it to an external API.

    Args:
        background_tasks (BackgroundTasks): Tasks to be executed in the background.
        db (Session): Database session dependency.

    Returns:
        JSONResponse: A response containing the exported customer data or an error message.

    """

    try:
        # Get the data to export from the database
        log.info("Starting data export from the database")
        exported_customers = export_database(db)
        log.info(f"Exported customers from the database")

        # Send the exported data to the external API
        log.info("Sending exported data to external API")
        status_code = await send_to_external_api(exported_customers)
        if status_code != 200:
            raise HTTPException(status_code=502, detail="Failed to send data to external API")

        log.info("Data successfully sent to external API")
        background_tasks.add_task(update_state_after_export, db)

        return JSONResponse(content={"exported_customers": exported_customers})
    except Exception as exc:
        logging.error(f"Unexpected error occurred: {exc}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred while exporting data")

