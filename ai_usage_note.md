This project leverages **Google Gemini AI** to perform financial reconciliation between ERP invoice data and bank statement transactions.

### 🔹 Why AI is Used

Traditional reconciliation scripts rely only on exact rule-based matching. However, real-world financial data often includes:

* **Date mismatches** 
* **Rounding differences** due to decimal precision.
* **Duplicate or partial entries** in bank records.
* **Textual variations** in transaction descriptions.

AI helps by:

* Parsing **semi-structured data** extracted from PDFs and ERP systems.
* Identifying and matching invoice numbers reliably, even if embedded in noisy text.
* Applying **tolerance rules** (e.g., distinguishing between rounding issues vs. actual mismatches).
* Generating a **business-friendly summary report** with insights and recommendations.

### 🔹 Role of Gemini AI in the Workflow

1. **Input**:

   * ERP data (JSON from Excel).
   * Bank statement tables (extracted from PDF).

2. **Processing with Gemini**:

   * Interprets both datasets.
   * Matches ERP invoices with corresponding bank transactions.
   * Classifies discrepancies (`Match`, `Amount mismatch`, `Rounding difference`, `Duplicate in Bank`, `Missing in Bank`).

3. **Output**:

   * Structured reconciliation in JSON → Converted into Excel (`reconciled_output.xlsx`).
   * Narrative business report (`reconciliation_report.md`).

### 🔹 Benefits of AI-Driven Reconciliation

* **Accuracy**: Reduces manual errors in reconciliation.
* **Efficiency**: Automates tedious cross-checking.
* **Explainability**: Provides a structured JSON + human-readable report.
* **Scalability**: Can handle large ERP and bank datasets.
