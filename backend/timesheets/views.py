from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime
from .models import TimeSheet, MonthlyTimeSheet, DailyEntry
from drivers.models import Driver
from cranes.models import Crane
from clients.models import Client


@login_required
def timesheet_list(request):
    timesheets = TimeSheet.objects.select_related('driver', 'crane', 'client').all()
    return render(request, 'timesheets/timesheet_list.html', {'timesheets': timesheets})


@login_required
def timesheet_create(request):
    if request.method == 'POST':
        try:
            date = request.POST.get('date')
            driver_id = request.POST.get('driver')
            crane_id = request.POST.get('crane')
            client_id = request.POST.get('client')
            start_time = request.POST.get('start_time')
            end_time = request.POST.get('end_time')
            notes = request.POST.get('notes', '')
            
            timesheet = TimeSheet.objects.create(
                date=date,
                driver_id=driver_id,
                crane_id=crane_id,
                client_id=client_id,
                start_time=start_time,
                end_time=end_time,
                notes=notes
            )
            
            messages.success(request, f'Time sheet created. Revenue: {timesheet.revenue} EGP, Driver Wage: {timesheet.driver_wage:.0f} EGP')
            return redirect('timesheet_list')
        except Exception as e:
            messages.error(request, f'Error creating time sheet: {str(e)}')
    
    context = {
        'timesheet': None,
        'drivers': Driver.objects.all(),
        'cranes': Crane.objects.all(),
        'clients': Client.objects.all(),
        'today': datetime.now().strftime('%Y-%m-%d'),
    }
    return render(request, 'timesheets/timesheet_form.html', context)


@login_required
def timesheet_edit(request, pk):
    timesheet = get_object_or_404(TimeSheet, pk=pk)
    
    if request.method == 'POST':
        try:
            timesheet.date = request.POST.get('date')
            timesheet.driver_id = request.POST.get('driver')
            timesheet.crane_id = request.POST.get('crane')
            timesheet.client_id = request.POST.get('client')
            timesheet.start_time = request.POST.get('start_time')
            timesheet.end_time = request.POST.get('end_time')
            timesheet.notes = request.POST.get('notes', '')
            timesheet.save()
            
            messages.success(request, 'Time sheet updated successfully.')
            return redirect('timesheet_list')
        except Exception as e:
            messages.error(request, f'Error updating time sheet: {str(e)}')
    
    context = {
        'timesheet': timesheet,
        'drivers': Driver.objects.all(),
        'cranes': Crane.objects.all(),
        'clients': Client.objects.all(),
    }
    return render(request, 'timesheets/timesheet_form.html', context)


@login_required
def timesheet_delete(request, pk):
    timesheet = get_object_or_404(TimeSheet, pk=pk)
    timesheet.delete()
    messages.success(request, 'Time sheet deleted successfully.')
    return redirect('timesheet_list')


@login_required
def timesheet_calculate(request):
    """AJAX endpoint for real-time calculation preview."""
    start_time = request.GET.get('start_time')
    end_time = request.GET.get('end_time')
    crane_id = request.GET.get('crane_id')
    driver_id = request.GET.get('driver_id')
    
    if not all([start_time, end_time]):
        return JsonResponse({'error': 'Missing time values'}, status=400)
    
    try:
        from datetime import datetime, timedelta
        from decimal import Decimal
        
        start = datetime.strptime(start_time, '%H:%M')
        end = datetime.strptime(end_time, '%H:%M')
        
        if end <= start:
            end += timedelta(days=1)
        
        diff = end - start
        total_hours = Decimal(str(diff.total_seconds() / 3600))
        
        # Determine shift type
        if total_hours <= 8:
            shift_type = '8h'
            overtime = Decimal('0')
        elif total_hours <= 9:
            shift_type = '9h'
            overtime = total_hours - Decimal('8')
        else:
            shift_type = '12h'
            overtime = total_hours - Decimal('8')
        
        result = {
            'total_hours': float(total_hours),
            'overtime_hours': float(overtime),
            'shift_type': shift_type,
        }
        
        # Calculate revenue if crane is provided
        if crane_id:
            try:
                crane = Crane.objects.get(pk=crane_id)
                if shift_type == '8h':
                    result['revenue'] = float(crane.rate_8h)
                elif shift_type == '9h':
                    result['revenue'] = float(crane.rate_9h)
                else:
                    result['revenue'] = float(crane.rate_12h)
                
                if crane.is_subrented:
                    result['commission'] = result['revenue'] - float(crane.owner_cost)
                else:
                    result['commission'] = result['revenue']
            except Crane.DoesNotExist:
                pass
        
        # Calculate driver wage if driver is provided
        if driver_id:
            try:
                driver = Driver.objects.get(pk=driver_id)
                daily_rate = float(driver.base_salary) / 30
                overtime_rate = daily_rate / 8 * 1.5
                result['driver_wage'] = daily_rate + (float(overtime) * overtime_rate)
            except Driver.DoesNotExist:
                pass
        
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


# ============================================
# Monthly Time Sheet Views (Hard Copy Format)
# ============================================

@login_required
def monthly_sheet_list(request):
    """List all monthly time sheets."""
    sheets = MonthlyTimeSheet.objects.select_related('driver', 'crane', 'client').all()
    return render(request, 'timesheets/monthly_list.html', {'sheets': sheets})


@login_required
def monthly_sheet_create(request):
    """Create a new monthly time sheet."""
    if request.method == 'POST':
        try:
            month = int(request.POST.get('month'))
            year = int(request.POST.get('year'))
            
            sheet = MonthlyTimeSheet.objects.create(
                client_id=request.POST.get('client'),
                crane_id=request.POST.get('crane'),
                driver_id=request.POST.get('driver'),
                location=request.POST.get('location', ''),
                month=month,
                year=year,
                supervisor_name=request.POST.get('supervisor_name', '')
            )
            
            messages.success(request, f'Monthly sheet created for {sheet.get_month_display()} {year}')
            return redirect('monthly_sheet_detail', pk=sheet.pk)
        except Exception as e:
            messages.error(request, f'Error creating sheet: {str(e)}')
    
    now = datetime.now()
    context = {
        'drivers': Driver.objects.all(),
        'cranes': Crane.objects.all(),
        'clients': Client.objects.all(),
        'current_month': now.month,
        'current_year': now.year,
        'years': range(now.year - 1, now.year + 2),
    }
    return render(request, 'timesheets/monthly_create.html', context)


@login_required
def monthly_sheet_detail(request, pk):
    """View and edit a monthly time sheet with 31-row table."""
    sheet = get_object_or_404(MonthlyTimeSheet.objects.select_related('driver', 'crane', 'client'), pk=pk)
    entries = sheet.daily_entries.all().order_by('day_number')
    
    context = {
        'sheet': sheet,
        'entries': entries,
    }
    return render(request, 'timesheets/monthly_detail.html', context)


@login_required
def monthly_sheet_delete(request, pk):
    """Delete a monthly time sheet."""
    sheet = get_object_or_404(MonthlyTimeSheet, pk=pk)
    month_name = f"{sheet.get_month_display()} {sheet.year}"
    sheet.delete()
    messages.success(request, f'Monthly sheet for {month_name} deleted.')
    return redirect('monthly_sheet_list')


@login_required
def daily_entry_update(request, pk):
    """AJAX endpoint to update a single daily entry."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    
    entry = get_object_or_404(DailyEntry, pk=pk)
    
    try:
        # Update fields from POST data
        from_time = request.POST.get('from_time')
        to_time = request.POST.get('to_time')
        trips = request.POST.get('trips', 0)
        notes = request.POST.get('notes', '')
        attendance_hours = request.POST.get('attendance_hours', 0)
        
        entry.from_time = from_time if from_time else None
        entry.to_time = to_time if to_time else None
        entry.trips = int(trips) if trips else 0
        entry.notes = notes
        entry.attendance_hours = float(attendance_hours) if attendance_hours else 0
        entry.save()
        
        return JsonResponse({
            'success': True,
            'operating_hours': float(entry.operating_hours),
            'monthly_totals': {
                'operating_hours': float(entry.monthly_sheet.total_operating_hours),
                'attendance_hours': float(entry.monthly_sheet.total_attendance_hours),
                'trips': entry.monthly_sheet.total_trips,
                'revenue': float(entry.monthly_sheet.total_revenue),
                'driver_wage': float(entry.monthly_sheet.total_driver_wage),
            }
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
def monthly_sheet_save_all(request, pk):
    """Save all daily entries at once from the form."""
    if request.method != 'POST':
        return redirect('monthly_sheet_detail', pk=pk)
    
    sheet = get_object_or_404(MonthlyTimeSheet, pk=pk)
    
    try:
        entries_updated = 0
        for entry in sheet.daily_entries.filter(date__isnull=False):
            prefix = f'entry_{entry.day_number}_'
            
            from_time = request.POST.get(f'{prefix}from_time', '').strip()
            from_period = request.POST.get(f'{prefix}from_period', 'AM')
            to_time = request.POST.get(f'{prefix}to_time', '').strip()
            to_period = request.POST.get(f'{prefix}to_period', 'PM')
            trips = request.POST.get(f'{prefix}trips', '').strip()
            notes = request.POST.get(f'{prefix}notes', '').strip()
            attendance = request.POST.get(f'{prefix}attendance', '').strip()
            
            # Only update if there's any data
            entry.from_time = from_time if from_time else None
            entry.from_period = from_period
            entry.to_time = to_time if to_time else None
            entry.to_period = to_period
            entry.trips = int(trips) if trips else 0
            entry.notes = notes
            entry.attendance_hours = float(attendance) if attendance else 0
            entry.save()
            entries_updated += 1
        
        # Always update supervisor name
        supervisor = request.POST.get('supervisor_name', '').strip()
        sheet.supervisor_name = supervisor
        sheet.calculate_totals()
        sheet.save()
        
        messages.success(request, f'تم حفظ البيانات بنجاح! ({entries_updated} يوم)')
    except Exception as e:
        messages.error(request, f'خطأ في الحفظ: {str(e)}')
    
    return redirect('monthly_sheet_detail', pk=pk)
