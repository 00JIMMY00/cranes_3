"""
PDF generation utilities using ReportLab.
"""
from io import BytesIO
from decimal import Decimal
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT


def generate_invoice_pdf(client, month, year, timesheets):
    """
    Generate a PDF invoice for a client for a specific month.
    
    Args:
        client: Client model instance
        month: Month number (1-12)
        year: Year (e.g., 2025)
        timesheets: QuerySet of TimeSheet entries for this client/month
    
    Returns:
        BytesIO buffer containing the PDF
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, 
                           rightMargin=1*cm, leftMargin=1*cm,
                           topMargin=1*cm, bottomMargin=1*cm)
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        alignment=TA_CENTER,
        spaceAfter=20,
    )
    header_style = ParagraphStyle(
        'Header',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=5,
    )
    
    elements = []
    
    # Title
    elements.append(Paragraph("INVOICE", title_style))
    elements.append(Spacer(1, 0.5*cm))
    
    # Month names
    months = ['', 'January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']
    month_name = months[month] if 1 <= month <= 12 else str(month)
    
    # Invoice header info
    header_data = [
        ['Invoice For:', f'{month_name} {year}'],
        ['Client:', client.name],
        ['Address:', client.address or 'N/A'],
    ]
    
    header_table = Table(header_data, colWidths=[3*cm, 14*cm])
    header_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 1*cm))
    
    # Time sheet entries table
    table_data = [['Date', 'Crane', 'Driver', 'Hours', 'Shift', 'Amount (EGP)']]
    
    total_amount = Decimal('0')
    for ts in timesheets:
        table_data.append([
            ts.date.strftime('%d/%m/%Y'),
            ts.crane.name,
            ts.driver.name,
            f'{ts.total_hours:.1f}',
            ts.get_shift_type_display(),
            f'{ts.revenue:,.0f}',
        ])
        total_amount += ts.revenue
    
    # Add total row
    table_data.append(['', '', '', '', 'TOTAL:', f'{total_amount:,.0f}'])
    
    col_widths = [2.5*cm, 4*cm, 4*cm, 2*cm, 2*cm, 3*cm]
    table = Table(table_data, colWidths=col_widths)
    table.setStyle(TableStyle([
        # Header row
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        
        # Data rows
        ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ALIGN', (3, 1), (-1, -1), 'RIGHT'),
        
        # Total row
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#ecf0f1')),
        
        # Grid
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor('#f8f9fa')]),
        
        # Padding
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 1*cm))
    
    # Footer
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_CENTER,
        textColor=colors.grey,
    )
    elements.append(Paragraph("Thank you for your business!", footer_style))
    elements.append(Paragraph("Cranes Management System", footer_style))
    
    doc.build(elements)
    buffer.seek(0)
    return buffer


def generate_wage_slip_pdf(driver, month, year, timesheets, loans):
    """
    Generate a PDF wage slip for a driver for a specific month.
    
    Args:
        driver: Driver model instance
        month: Month number (1-12)
        year: Year (e.g., 2025)
        timesheets: QuerySet of TimeSheet entries for this driver/month
        loans: QuerySet of Loan entries for this driver/month
    
    Returns:
        BytesIO buffer containing the PDF
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                           rightMargin=1*cm, leftMargin=1*cm,
                           topMargin=1*cm, bottomMargin=1*cm)
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        alignment=TA_CENTER,
        spaceAfter=20,
    )
    
    elements = []
    
    # Title
    elements.append(Paragraph("WAGE SLIP", title_style))
    elements.append(Spacer(1, 0.5*cm))
    
    # Month names
    months = ['', 'January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']
    month_name = months[month] if 1 <= month <= 12 else str(month)
    
    # Header info
    header_data = [
        ['Period:', f'{month_name} {year}'],
        ['Driver:', driver.name],
        ['Base Salary:', f'{driver.base_salary:,.0f} EGP/month'],
    ]
    
    header_table = Table(header_data, colWidths=[3*cm, 14*cm])
    header_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 0.5*cm))
    
    # Earnings section
    elements.append(Paragraph("<b>EARNINGS</b>", styles['Heading3']))
    
    earnings_data = [['Date', 'Client', 'Crane', 'Hours', 'Wage (EGP)']]
    total_wages = Decimal('0')
    
    for ts in timesheets:
        earnings_data.append([
            ts.date.strftime('%d/%m/%Y'),
            ts.client.name,
            ts.crane.name,
            f'{ts.total_hours:.1f}',
            f'{ts.driver_wage:,.0f}',
        ])
        total_wages += ts.driver_wage
    
    earnings_data.append(['', '', '', 'Total Earned:', f'{total_wages:,.0f}'])
    
    col_widths = [2.5*cm, 4*cm, 4*cm, 3*cm, 3*cm]
    earnings_table = Table(earnings_data, colWidths=col_widths)
    earnings_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27ae60')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ALIGN', (3, 1), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#d5f4e6')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(earnings_table)
    elements.append(Spacer(1, 0.5*cm))
    
    # Deductions section (Loans)
    elements.append(Paragraph("<b>DEDUCTIONS (Loans)</b>", styles['Heading3']))
    
    deductions_data = [['Date', 'Notes', 'Amount (EGP)']]
    total_loans = Decimal('0')
    
    for loan in loans:
        deductions_data.append([
            loan.date.strftime('%d/%m/%Y'),
            loan.notes or '-',
            f'{loan.amount:,.0f}',
        ])
        total_loans += loan.amount
    
    if not loans:
        deductions_data.append(['-', 'No loans this month', '0'])
    
    deductions_data.append(['', 'Total Deductions:', f'{total_loans:,.0f}'])
    
    col_widths = [3*cm, 10.5*cm, 3*cm]
    deductions_table = Table(deductions_data, colWidths=col_widths)
    deductions_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e74c3c')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ALIGN', (-1, 1), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#fadbd8')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(deductions_table)
    elements.append(Spacer(1, 1*cm))
    
    # Net Payable Summary
    net_payable = total_wages - total_loans
    
    summary_data = [
        ['Total Earned:', f'{total_wages:,.0f} EGP'],
        ['Less: Loans:', f'{total_loans:,.0f} EGP'],
        ['NET PAYABLE:', f'{net_payable:,.0f} EGP'],
    ]
    
    summary_table = Table(summary_data, colWidths=[8*cm, 5*cm])
    summary_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#3498db')),
        ('TEXTCOLOR', (0, -1), (-1, -1), colors.white),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('BOX', (0, 0), (-1, -1), 1, colors.grey),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 1*cm))
    
    # Signature line
    sig_style = ParagraphStyle(
        'Signature',
        parent=styles['Normal'],
        fontSize=10,
    )
    elements.append(Paragraph("_________________________", sig_style))
    elements.append(Paragraph("Driver Signature", sig_style))
    
    doc.build(elements)
    buffer.seek(0)
    return buffer
