from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, BackgroundTasks
from starlette.responses import JSONResponse

from display_interactive.backend.sqlite import get_db
from display_interactive.services.export import export_database, update_state_after_export, send_to_external_api

router = APIRouter(tags=["export"], prefix="")


@router.post("/send-customers")
async def export_data(
        background_tasks: BackgroundTasks,
        db: Session = Depends(get_db)
):
    """
    Export data from the database and send it to an external API.

    """

    try:
        # Get the data to export from the database
        exported_customers = await export_database(db)

        # Send the exported data to the external API
        status_code = await send_to_external_api(exported_customers)
        if status_code != 200:
            raise Exception("Failed to send data to external API")

        background_tasks.add_task(update_state_after_export, db)

        return JSONResponse(content={"exported_customers": exported_customers})
    except:
        raise Exception("An error occurred while exporting data")

