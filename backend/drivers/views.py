from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import viewsets
from datetime import date
from .models import Driver, Loan
from .serializers import DriverSerializer, LoanSerializer


class DriverViewSet(viewsets.ModelViewSet):
    """API endpoint for managing drivers."""
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer


class LoanViewSet(viewsets.ModelViewSet):
    """API endpoint for managing loans."""
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer


# Template-based views
@login_required
def driver_list(request):
    drivers = Driver.objects.all()
    return render(request, 'drivers/driver_list.html', {'drivers': drivers})


@login_required
def driver_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        base_salary = request.POST.get('base_salary', 0) or 0
        
        Driver.objects.create(
            name=name,
            base_salary=base_salary
        )
        messages.success(request, f'Driver "{name}" created successfully.')
        return redirect('driver_list')
    
    return render(request, 'drivers/driver_form.html', {'driver': None})


@login_required
def driver_edit(request, pk):
    driver = get_object_or_404(Driver, pk=pk)
    
    if request.method == 'POST':
        driver.name = request.POST.get('name')
        driver.base_salary = request.POST.get('base_salary', 0) or 0
        driver.save()
        messages.success(request, f'Driver "{driver.name}" updated successfully.')
        return redirect('driver_list')
    
    return render(request, 'drivers/driver_form.html', {'driver': driver})


@login_required
def driver_delete(request, pk):
    driver = get_object_or_404(Driver, pk=pk)
    name = driver.name
    driver.delete()
    messages.success(request, f'Driver "{name}" deleted successfully.')
    return redirect('driver_list')


@login_required
def driver_detail(request, pk):
    """Driver profile page with loans and wage history."""
    driver = get_object_or_404(Driver, pk=pk)
    loans = driver.loans.all()[:10]  # Recent 10 loans
    
    # Get wage summary from timesheets
    from timesheets.models import TimeSheet
    from django.db.models import Sum
    
    wage_summary = TimeSheet.objects.filter(driver=driver).aggregate(
        total_wages=Sum('driver_wage')
    )
    total_wages = wage_summary['total_wages'] or 0
    total_loans = driver.loans.aggregate(total=Sum('amount'))['total'] or 0
    
    context = {
        'driver': driver,
        'loans': loans,
        'total_wages': total_wages,
        'total_loans': total_loans,
    }
    return render(request, 'drivers/driver_detail.html', context)


# Loan views
@login_required
def loan_list(request):
    """List all loans with optional driver filter."""
    driver_id = request.GET.get('driver')
    loans = Loan.objects.select_related('driver').all()
    
    if driver_id:
        loans = loans.filter(driver_id=driver_id)
    
    drivers = Driver.objects.all()
    return render(request, 'loans/loan_list.html', {
        'loans': loans,
        'drivers': drivers,
        'selected_driver': driver_id,
    })


@login_required
def loan_create(request, driver_id=None):
    """Create a new loan, optionally for a specific driver."""
    drivers = Driver.objects.all()
    selected_driver = None
    
    if driver_id:
        selected_driver = get_object_or_404(Driver, pk=driver_id)
    
    if request.method == 'POST':
        driver_id = request.POST.get('driver')
        amount = request.POST.get('amount', 0) or 0
        loan_date = request.POST.get('date') or date.today()
        notes = request.POST.get('notes', '')
        
        driver = get_object_or_404(Driver, pk=driver_id)
        Loan.objects.create(
            driver=driver,
            amount=amount,
            date=loan_date,
            notes=notes
        )
        messages.success(request, f'Loan of {amount} EGP recorded for {driver.name}.')
        
        # Redirect back to driver detail if came from there
        if 'next' in request.POST:
            return redirect(request.POST['next'])
        return redirect('loan_list')
    
    return render(request, 'loans/loan_form.html', {
        'loan': None,
        'drivers': drivers,
        'selected_driver': selected_driver,
    })


@login_required
def loan_edit(request, pk):
    loan = get_object_or_404(Loan, pk=pk)
    drivers = Driver.objects.all()
    
    if request.method == 'POST':
        loan.driver_id = request.POST.get('driver')
        loan.amount = request.POST.get('amount', 0) or 0
        loan.date = request.POST.get('date') or date.today()
        loan.notes = request.POST.get('notes', '')
        loan.save()
        messages.success(request, 'Loan updated successfully.')
        return redirect('loan_list')
    
    return render(request, 'loans/loan_form.html', {
        'loan': loan,
        'drivers': drivers,
        'selected_driver': loan.driver,
    })


@login_required
def loan_delete(request, pk):
    loan = get_object_or_404(Loan, pk=pk)
    driver_name = loan.driver.name
    amount = loan.amount
    loan.delete()
    messages.success(request, f'Loan of {amount} EGP for {driver_name} deleted.')
    return redirect('loan_list')
