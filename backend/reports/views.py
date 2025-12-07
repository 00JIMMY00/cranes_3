from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from datetime import date

from clients.models import Client
from drivers.models import Driver, Loan
from timesheets.models import TimeSheet
from .pdf_utils import generate_invoice_pdf, generate_wage_slip_pdf


@login_required
def reports_dashboard(request):
    """Reports dashboard with links to generate invoices and wage slips."""
    clients = Client.objects.all()
    drivers = Driver.objects.all()
    
    # Get current month/year as defaults
    today = date.today()
    
    context = {
        'clients': clients,
        'drivers': drivers,
        'current_month': today.month,
        'current_year': today.year,
        'months': [
            (1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'),
            (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'),
            (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December'),
        ],
        'years': range(today.year - 2, today.year + 1),
    }
    return render(request, 'reports/dashboard.html', context)


@login_required
def generate_invoice(request):
    """Generate PDF invoice for a client/month."""
    client_id = request.GET.get('client')
    month = request.GET.get('month')
    year = request.GET.get('year')
    
    if not all([client_id, month, year]):
        return HttpResponse("Missing parameters: client, month, year required", status=400)
    
    try:
        month = int(month)
        year = int(year)
    except ValueError:
        return HttpResponse("Invalid month or year", status=400)
    
    client = get_object_or_404(Client, pk=client_id)
    
    # Get timesheets for this client/month
    timesheets = TimeSheet.objects.filter(
        client=client,
        date__month=month,
        date__year=year
    ).select_related('crane', 'driver').order_by('date')
    
    if not timesheets.exists():
        return HttpResponse(f"No time sheets found for {client.name} in {month}/{year}", status=404)
    
    # Generate PDF
    pdf_buffer = generate_invoice_pdf(client, month, year, timesheets)
    
    # Return PDF response
    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    filename = f"Invoice_{client.name.replace(' ', '_')}_{year}_{month:02d}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


@login_required
def generate_wage_slip(request):
    """Generate PDF wage slip for a driver/month."""
    driver_id = request.GET.get('driver')
    month = request.GET.get('month')
    year = request.GET.get('year')
    
    if not all([driver_id, month, year]):
        return HttpResponse("Missing parameters: driver, month, year required", status=400)
    
    try:
        month = int(month)
        year = int(year)
    except ValueError:
        return HttpResponse("Invalid month or year", status=400)
    
    driver = get_object_or_404(Driver, pk=driver_id)
    
    # Get timesheets for this driver/month
    timesheets = TimeSheet.objects.filter(
        driver=driver,
        date__month=month,
        date__year=year
    ).select_related('crane', 'client').order_by('date')
    
    # Get loans for this driver/month
    loans = Loan.objects.filter(
        driver=driver,
        date__month=month,
        date__year=year
    ).order_by('date')
    
    if not timesheets.exists() and not loans.exists():
        return HttpResponse(f"No records found for {driver.name} in {month}/{year}", status=404)
    
    # Generate PDF
    pdf_buffer = generate_wage_slip_pdf(driver, month, year, timesheets, loans)
    
    # Return PDF response
    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    filename = f"WageSlip_{driver.name.replace(' ', '_')}_{year}_{month:02d}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
