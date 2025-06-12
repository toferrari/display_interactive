### How install the project

- Create virtual environment with Python 3.9
```pyenv virtualenv 3.9 <env name> ```
- Activate the virtual environment
```pyenv activate <env name>```
- Install the requirements
```pip install -r requirements.txt```

Now you can run the project.

- Start the API
```uvicorn display_interactive.main:app --host 0.0.0.0 --port 8000 --reload```


### How to use the project
- You can see the API documentation at http://localhost:8000/docs and use the endpoints to interact with the API.

- Use curl to test the API 
For import  CSV files, you can use the following command:
```curl -X POST http://127.0.0.1:8000/import-csv \
    -H "Content-Type: application/json" \
    -d '{
    "customers_file_path": "display_interactive/csv_to_import/customers.csv",
    "purchases_file_path": "display_interactive/csv_to_import/purchases.csv"
    }'
   ```

For export the data to the external API
```curl -X POST http://127.0.0.1:8000/send-customers \
    -H "Content-Type: application/json"
   ```
    

### How to test it ?
Test are not implemented yet