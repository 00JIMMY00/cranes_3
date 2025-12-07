from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import viewsets
from .models import Client
from .serializers import ClientSerializer


class ClientViewSet(viewsets.ModelViewSet):
    """API endpoint for managing clients."""
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


# Template-based views
@login_required
def client_list(request):
    clients = Client.objects.all()
    return render(request, 'clients/client_list.html', {'clients': clients})


@login_required
def client_create(request):
    if request.method == 'POST':
        Client.objects.create(
            name=request.POST.get('name'),
            address=request.POST.get('address', ''),
            phone=request.POST.get('phone', ''),
            email=request.POST.get('email', '')
        )
        messages.success(request, 'Client created successfully.')
        return redirect('client_list')
    
    return render(request, 'clients/client_form.html', {'client': None})


@login_required
def client_edit(request, pk):
    client = get_object_or_404(Client, pk=pk)
    
    if request.method == 'POST':
        client.name = request.POST.get('name')
        client.address = request.POST.get('address', '')
        client.phone = request.POST.get('phone', '')
        client.email = request.POST.get('email', '')
        client.save()
        messages.success(request, f'Client "{client.name}" updated successfully.')
        return redirect('client_list')
    
    return render(request, 'clients/client_form.html', {'client': client})


@login_required
def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)
    name = client.name
    client.delete()
    messages.success(request, f'Client "{name}" deleted successfully.')
    return redirect('client_list')
