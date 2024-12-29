from fastapi import FastAPI, Form
from pydantic import BaseModel
import pandas as pd
import os

app = FastAPI()

# File path for the Excel file
EXCEL_FILE = "form_data.xlsx"

# Ensure the Excel file exists with proper headers
if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame(columns=["Name", "Email", "Message"])
    df.to_excel(EXCEL_FILE, index=False)

@app.post("/submit-form/")
async def submit_form(
    name: str = Form(...), 
    email: str = Form(...), 
    message: str = Form(...)
):
    # Append data to the Excel file
    try:
        new_data = {"Name": name, "Email": email, "Message": message}
        df = pd.read_excel(EXCEL_FILE)
        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
        df.to_excel(EXCEL_FILE, index=False)
        return {
            "message": "Form submitted and data saved to Excel successfully!",
            "data": new_data,
        }
    except Exception as e:
        return {"error": f"Failed to save data to Excel: {str(e)}"}

# Run the application with `uvicorn app:app --reload`
