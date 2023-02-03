import pandas as pd
import glob
from fpdf import FPDF
from pathlib import Path

filepaths = glob.glob("invoices/*xlsx")

for filepath in filepaths:
    pdf = FPDF(orientation='P', unit="mm", format="A4")
    pdf.add_page()

    filename = Path(filepath).stem
    invoice_no, date = filename.split("-")

    pdf.set_font(family="Times", size=16, style='B')
    pdf.cell(w=50, h=8, txt=f"Invoice no. {invoice_no}", ln=1)

    pdf.set_font(family="Times", size=16, style='B')
    pdf.cell(w=50, h=8, txt=f"Date: {date}", ln=1)

    df = pd.read_excel(filepath, sheet_name="Sheet 1")
    columns = list(df.columns)
    columns = [item.replace("_", " ").title() for item in columns]

    pdf.set_font(family="Times", size=12, style='B')
    pdf.set_text_color(100, 100, 100)

    # Add Header
    for i in range(0, len(columns) - 1):
        if i == 1 or i == 2:
            width = 50
        else:
            width = 30
        pdf.cell(w=width, h=8, txt=columns[i], border=1)

    pdf.cell(w=30, h=8, txt=columns[len(columns) - 1], border=1, ln=1)

    # Add Rows
    for index, row in df.iterrows():
        pdf.set_font(family="Times", size=10)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(w=30, h=8, txt=str(row["product_id"]), border=1)
        pdf.cell(w=50, h=8, txt=str(row["product_name"]), border=1)
        pdf.cell(w=50, h=8, txt=str(row["amount_purchased"]), border=1)
        pdf.cell(w=30, h=8, txt=str(row["price_per_unit"]), border=1)
        pdf.cell(w=30, h=8, txt=str(row["total_price"]), border=1, ln=1)

    pdf.output(f"PDFs/{filename}.pdf")
