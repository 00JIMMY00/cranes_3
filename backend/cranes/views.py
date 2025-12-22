from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import viewsets
from .models import Crane
from .serializers import CraneSerializer
from datetime import date


class CraneViewSet(viewsets.ModelViewSet):
    """API endpoint for managing cranes."""
    queryset = Crane.objects.all()
    serializer_class = CraneSerializer


# Template-based views
@login_required
def crane_list(request):
    cranes = Crane.objects.all()
    return render(request, 'cranes/crane_list.html', {'cranes': cranes})


@login_required
def crane_detail(request, pk):
    """View crane details including assignment history."""
    crane = get_object_or_404(Crane, pk=pk)
    today = date.today()
    
    # Get all assignments for this crane
    all_assignments = crane.monthly_sheets.select_related('client', 'driver').order_by('start_date')
    
    # Categorize assignments
    present = []
    future = []
    history = []
    
    for assignment in all_assignments:
        if assignment.start_date and assignment.end_date:
            if assignment.start_date <= today <= assignment.end_date:
                present.append(assignment)
            elif assignment.start_date > today:
                future.append(assignment)
            elif assignment.end_date < today:
                history.append(assignment)
        elif assignment.start_date:
            # No end_date, consider as ongoing if started
            if assignment.start_date <= today:
                present.append(assignment)
            else:
                future.append(assignment)
        else:
            # No dates set, put in history as legacy
            history.append(assignment)
    
    # Sort history in reverse (most recent first)
    history.reverse()
    
    return render(request, 'cranes/crane_detail.html', {
        'crane': crane,
        'present': present,
        'future': future,
        'history': history,
        'today': today,
    })


@login_required
def crane_create(request):
    if request.method == 'POST':
        Crane.objects.create(
            name=request.POST.get('name'),
            is_subrented='is_subrented' in request.POST,
            owner_cost=request.POST.get('owner_cost', 0) or 0
        )
        messages.success(request, 'Crane created successfully.')
        return redirect('crane_list')
    
    return render(request, 'cranes/crane_form.html', {'crane': None})


@login_required
def crane_edit(request, pk):
    crane = get_object_or_404(Crane, pk=pk)
    
    if request.method == 'POST':
        crane.name = request.POST.get('name')
        crane.is_subrented = 'is_subrented' in request.POST
        crane.owner_cost = request.POST.get('owner_cost', 0) or 0
        crane.save()
        messages.success(request, f'Crane "{crane.name}" updated successfully.')
        return redirect('crane_list')
    
    return render(request, 'cranes/crane_form.html', {'crane': crane})


@login_required
def crane_delete(request, pk):
    crane = get_object_or_404(Crane, pk=pk)
    name = crane.name
    crane.delete()
    messages.success(request, f'Crane "{name}" deleted successfully.')
    return redirect('crane_list')

