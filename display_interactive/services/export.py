import httpx
from sqlalchemy.orm import Session

from display_interactive.services.contant import API_EXTERNE_URL
from display_interactive.models.model import Customers, Purchases


async def export_database(db: Session):
    """
    Export data from the database to a CSV file.
    """
    customers = db.query(Customers).where(Customers.submitted == False).all()

    # Create a list of dictionaries for each customer with their purchases
    customers_dict = [customer.to_dict() for customer in customers]
    return customers_dict


def update_state_after_export(db: Session):
    """
    If the export to external API is successful, update the state of the customers and purchases to submitted.
    """
    db.query(Customers).filter(Customers.submitted == False).update({"submitted": True})
    db.query(Purchases).filter(Purchases.submitted == False).update({"submitted": True})
    db.commit()
    return


async def send_to_external_api(customers_data: list):
    """
    Send the exported customers data to an external API.
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(API_EXTERNE_URL, json={"exported_customers": customers_data})

        return response.status_code