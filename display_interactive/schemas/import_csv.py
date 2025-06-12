from pydantic import BaseModel


class ImportCSV(BaseModel):
    customers_file_path: str = "display_interactive/csv_to_import/customers.csv"
    purchases_file_path: str = "display_interactive/csv_to_import/purchases.csv"