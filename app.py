import pandas as pd
from google import genai
from google.genai import types
import pathlib
from dotenv import load_dotenv
import os
import json
import pdfplumber

# Load environment variables from a .env file
# Ensure you have a .env file with your GOOGLE_API_KEY
load_dotenv()

def reconcile_with_gemini(erp_data_json: str, pdf_filepath: pathlib.Path) -> str:
    """
    Reconciles ERP data with a bank statement PDF using the Gemini model.

    Args:
        erp_data_json (str): The ERP data formatted as a JSON string.
        pdf_filepath (pathlib.Path): The path to the bank statement PDF file.

    Returns:
        str: The file path of the generated Excel file, or None if an error occurs.
    """
    try:
        # Extract text from the PDF using pdfplumber
        with pdfplumber.open(pdf_filepath) as pdf:
            tables = []
            for page in pdf.pages:
                table = page.extract_table()
                if table:
                    df_page = pd.DataFrame(table[1:], columns=table[0])
                    tables.append(df_page)


        bank_statement = tables
        # Set up the API client
        # This uses the API key from your .env file
        api_key = os.getenv("GOOGLE_API_KEY")

        client = genai.Client()
        content = f"""Here is the ERP data:
            {erp_data_json}

            Here is the extracted text from the bank statement:
            {bank_statement}"""

        # Construct the detailed prompt for the model, including the extracted bank text
        prompt = """
You are a meticulous financial analyst. Your task is to reconcile two datasets:
1. ERP data provided as extracted text from an Excel file.
2. A bank statement provided as extracted text from a PDF.

Input:
Here is the ERP data:
{erp_data_json}

Here is the extracted text from the bank statement:
{bank_statement}

Please analyze both the ERP data and the bank statement text. Parse the ERP data into a list of transactions with Date, Invoice ID, Amount, Status. Parse the bank statement into a list of payment transactions (only those with Description starting with "Payment INV" - ignore Adjustments, Interests, Bank Fees, etc.). Match based on Invoice ID (INVxxxx), regardless of date differences. For each ERP entry, find corresponding bank entries with the same Invoice ID.

For each ERP transaction, compute:
- Amount_bank: Sum of all matching bank amounts for that Invoice ID.
- Bank Count: Number of matching bank entries for that Invoice ID.
- Discrepancy: Classify as follows:
  - "Match" if Bank Count == 1 and ERP Amount == Bank Amount (allow tolerance of 0.01 for floating point).
  - "Amount mismatch" if Bank Count == 1 and abs(ERP Amount - Bank Amount) > 1.
  - "Rounding difference" if Bank Count == 1 and 0 < abs(ERP Amount - Bank Amount) <= 1.
  - "Duplicate in Bank" if Bank Count > 1.
  - "Missing in Bank" if Bank Count == 0.
- Mismatch Amount: ERP Amount - Amount_bank (signed difference; 0 for exact matches).

Produce a reconciled report only for the ERP transactions (do not include bank-only entries like fees). Output in JSON format as an array of objects, sorted by Invoice ID.

The final JSON output must include these keys for each object:
- "Date": The date from ERP (YYYY-MM-DD).
- "Invoice ID": The invoice identifier.
- "Amount": The amount from ERP.
- "Status": The status from ERP (Paid, Pending, Cancelled).
- "Amount_bank": The summed amount from bank (0 if missing).
- "Bank Count": The count of bank entries.
- "Discrepancy": As classified above.
- "Mismatch Amount": The signed difference (Amount - Amount_bank).

Example JSON output:
```json
[
  {
    "Date": "2025-02-10",
    "Invoice ID": "INV0001",
    "Amount": 267.1,
    "Status": "Cancelled",
    "Amount_bank": 267.1,
    "Bank Count": 1,
    "Discrepancy": "Match",
    "Mismatch Amount": 0.0
  },
  {
    "Date": "2025-02-17",
    "Invoice ID": "INV0002",
    "Amount": 1789.75,
    "Status": "Paid",
    "Amount_bank": 1788.62,
    "Bank Count": 1,
    "Discrepancy": "Amount mismatch",
    "Mismatch Amount": 1.13
  },
  {
    "Date": "2025-01-02",
    "Invoice ID": "INV0003",
    "Amount": 1144.43,
    "Status": "Cancelled",
    "Amount_bank": 1144.43,
    "Bank Count": 1,
    "Discrepancy": "Match",
    "Mismatch Amount": 0.0
  }
]
```
Return ONLY the final reconciled data as a single JSON array of objects. Do not include any other text or explanations.
        """

        # Generate content using the text prompt 
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=[prompt, content]
        )

        # Clean the response to ensure it's valid JSON
        json_response_text = response.text.strip().replace('```json', '').replace('```', '').strip()
        print(json_response_text)
        # Parse the JSON string into a Python list of dictionaries
        reconciled_data = json.loads(json_response_text)

        # Convert the data into a pandas DataFrame for easy handling
        df = pd.DataFrame(reconciled_data)

        # Define the output filename and save to Excel
        output_filename = 'reconciled_output.xlsx'
        df.to_excel(output_filename, index=False)



        summary_prompt = f"""Please write a short report (1-2 pages worth of content) on the following reconciliation results. 
        Based on the give data:{json_response_text}
    Structure the report with these sections:
    - Introduction: A brief overview of the reconciliation process that was performed.
    - Overall Reconciliation Rate: 
    - Summary of Issues Found: Use the following data to summarize the discrepancies. A table is appropriate here. 
    - Detailed Findings: Briefly highlight examples for each category of issue: amount mismatches, duplicates, missing entries, and rounding differences.
    - Recommendations: Suggest concrete actions, such as investigating specific mismatches, reviewing payment cancellation processes, and checking for systematic rounding errors."""


        response_summary = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=[summary_prompt]
        )

        response_summary = response_summary.text.strip()
        with open("reconciliation_report.md", 'w') as f:
            f.write(response_summary)

        
        return output_filename

    except Exception as e:
        print(f"An error occurred during the reconciliation process: {e}")
        return None

# --- Main execution block ---
if __name__ == "__main__":
    # Define the paths to your input files
    erp_file = 'erp_data (1).xlsx'
    bank_statement_file = pathlib.Path('bank_statement (1).pdf')

    # --- Input File Validation ---
    if not os.path.exists(erp_file):
        print(f"FATAL ERROR: ERP data file not found at '{erp_file}'")
    elif not bank_statement_file.exists():
        print(f"FATAL ERROR: Bank statement PDF not found at '{bank_statement_file}'")
    else:
        print("Input files found. Starting reconciliation process...")
        
        # --- Data Preparation ---
        # Read the ERP data from the Excel file
        erp_df = pd.read_excel(erp_file)
        # Convert the DataFrame to a JSON string in a record-oriented format
        erp_json_string = erp_df.to_json(orient='records')

        # --- Function Call ---
        # Call the main function to perform reconciliation
        result_file_path = reconcile_with_gemini(erp_json_string, bank_statement_file)

        # --- Output ---
        if result_file_path:
            print(f"✅ Reconciliation successful!")
            print(f"Output saved to: '{result_file_path}'")
        else:
            print("❌ Reconciliation failed. Please review the error messages.")