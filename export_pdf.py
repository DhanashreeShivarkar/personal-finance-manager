# export_pdf.py
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    Table, TableStyle, Paragraph, SimpleDocTemplate, Spacer, HRFlowable, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import datetime
import sqlite3
import os

def export_monthly_report_pdf(user_id, month=None, year=None, filename=None):
    from reports import monthly_financial_report

    # Get report data from your reports module
    result = monthly_financial_report(user_id, month, year)
    month = result["month"]
    year = result["year"]

    filename = filename or f"monthly_report_{user_id}_{month}_{year}.pdf"

    # --- PDF setup ---
    doc = SimpleDocTemplate(
        filename, pagesize=A4,
        rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=30
    )
    elements = []
    styles = getSampleStyleSheet()
    
    # Add logo 
    logo_path = "assets/logo_innob.jpeg"  # logo path
    if os.path.exists(logo_path):
        logo = Image(logo_path)
        logo.drawHeight = 1.0 * inch  # height in inches
        logo.drawWidth = 3.5 * inch   # width in inches (slightly larger for visibility)
        logo.hAlign = "CENTER"
        elements.append(logo)
        elements.append(Spacer(1, 0.25 * inch))

    # --- Custom Styles ---
    styles.add(ParagraphStyle(name="SectionHeader", fontSize=14, textColor=colors.HexColor("#004B8D"), spaceAfter=10, spaceBefore=15, leading=16))
    styles.add(ParagraphStyle(name="NormalBold", fontSize=12, leading=14, textColor=colors.black, spaceAfter=6, spaceBefore=6))
    styles.add(ParagraphStyle(name="Footer", fontSize=9, textColor=colors.grey, alignment=1))

    # --- Header ---
    header_title = Paragraph(f"<b>Personal Finance Manager</b>", styles["Title"])
    subtitle = Paragraph(f"Monthly Financial Report - {month}/{year}", styles["Normal"])
    elements.append(header_title)
    elements.append(subtitle)
    elements.append(Spacer(1, 0.1 * inch))
    elements.append(HRFlowable(width="100%", color=colors.HexColor("#004B8D"), thickness=1))
    elements.append(Spacer(1, 0.2 * inch))

    # --- Summary Section ---
    elements.append(Paragraph("📊 <b>Financial Summary</b>", styles["SectionHeader"]))

    # Table data
    summary_data = [
        ["Metric", "Amount (₹)"],
        ["Total Income", f"{result['income']:.2f}"],
        ["Total Expenses", f"{result['expenses']:.2f}"],
        ["Net Savings", f"{result['savings']:.2f}"],
    ]

    # Style based on savings (green/red)
    savings_color = colors.HexColor("#009E60") if result["savings"] >= 0 else colors.HexColor("#B22222")

    summary_table = Table(summary_data, hAlign="LEFT", colWidths=[200, 200])
    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#004B8D")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("TEXTCOLOR", (1, 3), (1, 3), savings_color),
        ("BACKGROUND", (0, 3), (-1, 3), colors.whitesmoke),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 0.3 * inch))

    # --- Category-wise Breakdown ---
    elements.append(Paragraph("📂 <b>Category-wise Expenses</b>", styles["SectionHeader"]))

    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT category, IFNULL(SUM(amount), 0)
            FROM expenses
            WHERE user_id = ? AND strftime('%m', date)=printf('%02d', ?) AND strftime('%Y', date)=?
            GROUP BY category
        """, (user_id, month, str(year)))
        cat_rows = cursor.fetchall()

    if cat_rows:
        cat_data = [["Category", "Total (₹)"]] + [(c, f"{s:.2f}") for c, s in cat_rows]
        cat_table = Table(cat_data, hAlign="LEFT", colWidths=[200, 200])
        cat_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
        ]))
        elements.append(cat_table)
    else:
        elements.append(Paragraph("<i>No category expenses found for this month.</i>", styles["Normal"]))

    elements.append(Spacer(1, 0.4 * inch))

    # --- Footer ---
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    footer_text = f"Generated on {timestamp} | Powered by Innobyte Services | Personal Finance Manager"
    elements.append(HRFlowable(width="100%", color=colors.HexColor("#004B8D"), thickness=0.8))
    elements.append(Spacer(1, 0.1 * inch))
    elements.append(Paragraph(footer_text, styles["Footer"]))

    # --- Build the PDF ---
    doc.build(elements)
    print(f"PDF report successfully exported to: {filename}")
