# ERP vs Bank Statement Reconciliation with Gemini AI

This project automates the reconciliation of **ERP invoice data** with **bank statement transactions** using **Google Gemini AI**. It extracts transaction details from both sources, compares them, classifies discrepancies, and produces both an **Excel output** and a **summary reconciliation report**.

---

## 📌 Features

* Extracts **ERP data** from an Excel file.
* Extracts **bank statement transactions** from a PDF using `pdfplumber`.
* Uses **Gemini AI** to reconcile transactions:

  * Matches invoices by `Invoice ID`.
  * Computes mismatch amounts.
  * Classifies discrepancies (`Match`, `Amount mismatch`, `Rounding difference`, `Duplicate in Bank`, `Missing in Bank`).
* Exports results to:

  * `reconciled_output.xlsx` – structured reconciliation output.
  * `reconciliation_report.md` – summary report with insights and recommendations.

---

## 📂 Project Structure

```
.
├── erp_data (1).xlsx           # Sample ERP input file
├── bank_statement (1).pdf      # Sample bank statement input file
├── reconciliation.py           # Main reconciliation script
├── reconciled_output.xlsx      # Generated output (Excel format)
├── reconciliation_report.md    # Generated reconciliation summary report
├── .env                        # Contains GOOGLE_API_KEY
└── README.md                   # Project documentation
```

---

## ⚙️ Installation

1. Clone the repository or copy project files.
2. Install required dependencies:

   ```bash
   pip install pandas google-genai pdfplumber python-dotenv openpyxl
   ```
3. Set up your **Google API Key**:

   * Create a `.env` file in the project root.
   * Add the following line:

     ```
     GOOGLE_API_KEY=your_google_api_key_here
     ```

---

## 🚀 Usage

Run the script from the terminal:

```bash
python app.py
```

### Expected Workflow:

1. **Load ERP Data** → Extract transactions from Excel.
2. **Load Bank Statement** → Extract tables from PDF.
3. **Reconcile Data** → Use Gemini AI to classify discrepancies.
4. **Generate Reports** →

   * `reconciled_output.xlsx` → Full reconciliation details.
   * `reconciliation_report.md` → Business-friendly summary report.

---

## 📊 Example Output

### Excel (`reconciled_output.xlsx`)

| Date       | Invoice ID | Amount  | Status    | Amount\_bank | Bank Count | Discrepancy     | Mismatch Amount |
| ---------- | ---------- | ------- | --------- | ------------ | ---------- | --------------- | --------------- |
| 2025-02-10 | INV0001    | 267.10  | Cancelled | 267.10       | 1          | Match           | 0.0             |
| 2025-02-17 | INV0002    | 1789.75 | Paid      | 1788.62      | 1          | Amount mismatch | 1.13            |
| 2025-01-02 | INV0003    | 1144.43 | Cancelled | 1144.43      | 1          | Match           | 0.0             |

### Markdown Report (`reconciliation_report.md`)

* **Introduction** → Brief overview of reconciliation process.
* **Overall Reconciliation Rate** → % of transactions matched.
* **Summary of Issues Found** → Discrepancies by type.
* **Detailed Findings** → Highlight of mismatches, duplicates, missing, rounding.
* **Recommendations** → Suggested next steps.

---

## ✅ Future Enhancements

* Add support for **multi-currency reconciliation**.
* Improve **date tolerance** for near matches.
* Add **visual dashboard** for discrepancies.
* Enable **direct database integration** for ERP and bank data.

---

## 📝 License

This project is for **educational and internal use only**.

---

Do you want me to also create a **sample reconciliation\_report.md** file (filled with dummy findings), so it looks like a real-world output when someone first runs your project?
