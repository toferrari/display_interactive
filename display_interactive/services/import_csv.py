import pandas as pd
from sqlalchemy.orm import Session

from display_interactive.models.model import Purchases, Customers
from display_interactive.schemas.import_csv import ImportCSV


async def import_csv(path: ImportCSV, db: Session):
    customer_df = pd.read_csv(path.customers_file_path, sep=';')
    customer_df.replace("", float("NaN"), inplace=True)
    customer_df = customer_df.dropna(how='all', subset=['title', 'lastname', 'firstname', 'postal_code', 'email'])

    for index, row in customer_df.iterrows():
        customer = Customers(
            customer_id=row['customer_id'],
            title=row['title'],
            last_name=row['lastname'],
            first_name=row['firstname'],
            postal_code=row['postal_code'],
            email=row['email']
        )
        db.add(customer)

    purchases_df = pd.read_csv(path.purchases_file_path, sep=';')

    for index, row in purchases_df.iterrows():
        purchase = Purchases(
            customer_id=row['customer_id'],
            product_id=row['product_id'],
            quantity=row['quantity'],
            price=row['price'],
            currency=row['currency'],
            date=row['date']
        )
        db.add(purchase)

    db.commit()