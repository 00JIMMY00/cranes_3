from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import viewsets
from .models import Crane
from .serializers import CraneSerializer


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
def crane_create(request):
    if request.method == 'POST':
        Crane.objects.create(
            name=request.POST.get('name'),
            rate_8h=request.POST.get('rate_8h', 0) or 0,
            rate_9h=request.POST.get('rate_9h', 0) or 0,
            rate_12h=request.POST.get('rate_12h', 0) or 0,
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
        crane.rate_8h = request.POST.get('rate_8h', 0) or 0
        crane.rate_9h = request.POST.get('rate_9h', 0) or 0
        crane.rate_12h = request.POST.get('rate_12h', 0) or 0
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
