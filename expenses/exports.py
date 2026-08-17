"""
PDF and Excel export utilities.

Uses:
- ReportLab (Professional PDF layout with executive headers, KPIs, and zebra tables)
- OpenPyXL (Executive Excel formatting with styled banners, KPIs, currency format, auto-column widths)
"""

from io import BytesIO
from datetime import datetime
from django.http import HttpResponse

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable


def generate_pdf(expenses, user):
    """
    Generate an executive, professional PDF financial report.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )

    styles = getSampleStyleSheet()

    # Custom typography styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=4,
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#64748B'),
        spaceAfter=15,
    )

    meta_style = ParagraphStyle(
        'MetaText',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#0F172A'),
    )

    header_cell_style = ParagraphStyle(
        'HeaderCell',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=12,
        textColor=colors.white,
        alignment=0,
    )

    cell_style = ParagraphStyle(
        'BodyCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#1E293B'),
    )

    cell_style_right = ParagraphStyle(
        'BodyCellRight',
        parent=cell_style,
        alignment=2,
    )

    elements = []

    # 1. Header Banner Title
    elements.append(Paragraph("NOVASPEND FINANCIAL LEDGER", title_style))
    elements.append(Paragraph(f"Official Monthly Expense Statement &bull; Generated for <b>{user.username}</b> on {datetime.now().strftime('%B %d, %Y')}", subtitle_style))
    elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#10B981'), spaceAfter=15))

    # 2. Executive KPI Box
    total_amount = sum(float(e.amount) for e in expenses)
    total_count = len(expenses)
    avg_amount = (total_amount / total_count) if total_count > 0 else 0.0

    kpi_data = [
        [
            Paragraph(f"<b>TOTAL EXPENSES</b><br/><font size=14 color='#10B981'><b>₹{total_amount:,.2f}</b></font>", meta_style),
            Paragraph(f"<b>TOTAL TRANSACTIONS</b><br/><font size=14 color='#6366F1'><b>{total_count}</b></font>", meta_style),
            Paragraph(f"<b>AVERAGE ITEM</b><br/><font size=14 color='#06B6D4'><b>₹{avg_amount:,.2f}</b></font>", meta_style),
        ]
    ]

    kpi_table = Table(kpi_data, colWidths=[170, 170, 170])
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#E2E8F0')),
        ('INNERGRID', (0, 0), (-1, -1), 1, colors.HexColor('#E2E8F0')),
        ('PADDING', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(kpi_table)
    elements.append(Spacer(1, 18))

    # 3. Itemized Ledger Table
    table_data = [
        [
            Paragraph("Date", header_cell_style),
            Paragraph("Title / Merchant", header_cell_style),
            Paragraph("Category", header_cell_style),
            Paragraph("Method", header_cell_style),
            Paragraph("Amount (₹)", ParagraphStyle('HRight', parent=header_cell_style, alignment=2)),
        ]
    ]

    for expense in expenses:
        cat_name = expense.category.name if expense.category else "General"
        table_data.append([
            Paragraph(expense.expense_date.strftime("%b %d, %Y"), cell_style),
            Paragraph(expense.title, cell_style),
            Paragraph(cat_name, cell_style),
            Paragraph(expense.payment_method, cell_style),
            Paragraph(f"₹{expense.amount:,.2f}", cell_style_right),
        ])

    # Grand Total Row
    total_cell_left = Paragraph("<b>GRAND TOTAL</b>", ParagraphStyle('TotLeft', parent=cell_style, fontName='Helvetica-Bold', textColor=colors.HexColor('#065F46')))
    total_cell_right = Paragraph(f"<b>₹{total_amount:,.2f}</b>", ParagraphStyle('TotRight', parent=cell_style_right, fontName='Helvetica-Bold', textColor=colors.HexColor('#065F46')))
    table_data.append([
        total_cell_left, "", "", "", total_cell_right
    ])

    col_widths = [80, 175, 120, 75, 70]
    ledger_table = Table(table_data, colWidths=col_widths, repeatRows=1)

    t_style = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F172A')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        # Zebra Striping
        ('BACKGROUND', (0, 1), (-1, -2), colors.white),
        ('LINEBELOW', (0, 1), (-1, -2), 0.5, colors.HexColor('#F1F5F9')),
        # Grand Total Row Styling
        ('SPAN', (0, -1), (3, -1)),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#ECFDF5')),
        ('LINEABOVE', (0, -1), (-1, -1), 1.5, colors.HexColor('#10B981')),
        ('LINEBELOW', (0, -1), (-1, -1), 1.5, colors.HexColor('#10B981')),
    ]

    # Add zebra striping for alternate rows
    for r in range(1, len(table_data) - 1):
        if r % 2 == 0:
            t_style.append(('BACKGROUND', (0, r), (-1, r), colors.HexColor('#F8FAFC')))

    ledger_table.setStyle(TableStyle(t_style))
    elements.append(ledger_table)

    elements.append(Spacer(1, 20))
    footer_text = Paragraph(f"<font color='#94A3B8' size=8>NovaSpend Executive Ledger &bull; Confirmed Official Document &bull; User: {user.username}</font>", ParagraphStyle('Foot', parent=subtitle_style, alignment=1))
    elements.append(footer_text)

    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="NovaSpend_Expense_Report_{datetime.now().strftime("%Y%m%d")}.pdf"'
    return response


def generate_excel(expenses, user):
    """
    Generate an executive Excel spreadsheet report.
    """
    wb = Workbook()
    ws = wb.active
    ws.title = "Expense Report"
    ws.views.sheetView[0].showGridLines = True

    # Color Tokens
    COLOR_HEADER_BG = "0F172A"
    COLOR_TH_BG = "10B981"
    COLOR_ZEBRA = "F8FAFC"
    COLOR_TOTAL_BG = "ECFDF5"

    # Styles
    font_title = Font(name="Calibri", size=16, bold=True, color="FFFFFF")
    font_sub = Font(name="Calibri", size=10, italic=True, color="94A3B8")
    font_header = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    font_bold = Font(name="Calibri", size=11, bold=True, color="0F172A")
    font_regular = Font(name="Calibri", size=11, color="1E293B")
    font_total = Font(name="Calibri", size=11, bold=True, color="065F46")

    fill_title = PatternFill(start_color=COLOR_HEADER_BG, end_color=COLOR_HEADER_BG, fill_type="solid")
    fill_th = PatternFill(start_color=COLOR_TH_BG, end_color=COLOR_TH_BG, fill_type="solid")
    fill_zebra = PatternFill(start_color=COLOR_ZEBRA, end_color=COLOR_ZEBRA, fill_type="solid")
    fill_total = PatternFill(start_color=COLOR_TOTAL_BG, end_color=COLOR_TOTAL_BG, fill_type="solid")

    thin_side = Side(border_style="thin", color="CBD5E1")
    border_all = Border(left=thin_side, right=thin_side, top=thin_side, bottom=thin_side)
    border_total = Border(top=Side(border_style="medium", color="10B981"), bottom=Side(border_style="double", color="10B981"))

    # 1. Title Banner Block
    ws.merge_cells("A1:F1")
    ws["A1"] = "NOVASPEND EXECUTIVE EXPENSE STATEMENT"
    ws["A1"].font = font_title
    ws["A1"].fill = fill_title
    ws["A1"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[1].height = 35

    ws.merge_cells("A2:F2")
    ws["A2"] = f"Generated for {user.username} on {datetime.now().strftime('%B %d, %Y - %I:%M %p')}"
    ws["A2"].font = font_sub
    ws["A2"].fill = fill_title
    ws["A2"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[2].height = 20

    # 2. Table Header
    headers = ["Date", "Title / Merchant", "Category", "Amount (₹)", "Payment Method", "Notes"]
    ws.row_dimensions[4].height = 26

    for col_idx, text in enumerate(headers, 1):
        cell = ws.cell(row=4, column=col_idx, value=text)
        cell.font = font_header
        cell.fill = fill_th
        cell.alignment = Alignment(horizontal="center" if col_idx in [1, 5] else ("right" if col_idx == 4 else "left"), vertical="center")
        cell.border = border_all

    # 3. Data Rows
    row_idx = 5
    total_amount = 0.0

    for expense in expenses:
        amt = float(expense.amount)
        total_amount += amt
        cat_name = expense.category.name if expense.category else "General"

        r_cells = [
            ws.cell(row=row_idx, column=1, value=expense.expense_date.strftime("%d-%m-%Y")),
            ws.cell(row=row_idx, column=2, value=expense.title),
            ws.cell(row=row_idx, column=3, value=cat_name),
            ws.cell(row=row_idx, column=4, value=amt),
            ws.cell(row=row_idx, column=5, value=expense.payment_method),
            ws.cell(row=row_idx, column=6, value=expense.notes or ""),
        ]

        ws.row_dimensions[row_idx].height = 22

        for c_idx, c in enumerate(r_cells, 1):
            c.font = font_regular
            c.border = border_all
            c.alignment = Alignment(vertical="center", horizontal="center" if c_idx in [1, 5] else ("right" if c_idx == 4 else "left"))
            if row_idx % 2 == 1:
                c.fill = fill_zebra
            if c_idx == 4:
                c.number_format = '"₹"#,##0.00'

        row_idx += 1

    # 4. Grand Total Row
    ws.row_dimensions[row_idx + 1].height = 26
    ws.merge_cells(start_row=row_idx + 1, start_column=1, end_row=row_idx + 1, end_column=3)

    tot_label = ws.cell(row=row_idx + 1, column=1, value="GRAND TOTAL")
    tot_label.font = font_total
    tot_label.alignment = Alignment(horizontal="right", vertical="center")

    tot_val = ws.cell(row=row_idx + 1, column=4, value=total_amount)
    tot_val.font = font_total
    tot_val.number_format = '"₹"#,##0.00'
    tot_val.alignment = Alignment(horizontal="right", vertical="center")

    for col in range(1, 7):
        cell = ws.cell(row=row_idx + 1, column=col)
        cell.fill = fill_total
        cell.border = border_total

    # 5. Auto Column Widths
    for col in ws.columns:
        max_len = max(len(str(cell.value or '')) for cell in col)
        col_letter = get_column_letter(col[0].column)
        ws.column_dimensions[col_letter].width = max(max_len + 4, 14)

    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = f'attachment; filename="NovaSpend_Expense_Report_{datetime.now().strftime("%Y%m%d")}.xlsx"'
    wb.save(response)
    return response