from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Client, Payment
from .serializers import ClientSerializer, PaymentSerializer


class ClientViewSet(viewsets.ModelViewSet):
    """API endpoint for managing clients."""
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    
    @action(detail=True, methods=['get', 'post'])
    def payments(self, request, pk=None):
        """List or create payments for a specific client."""
        client = self.get_object()
        
        if request.method == 'GET':
            payments = client.payments.all()
            serializer = PaymentSerializer(payments, many=True)
            return Response(serializer.data)
        
        elif request.method == 'POST':
            serializer = PaymentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(client=client)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentViewSet(viewsets.ModelViewSet):
    """API endpoint for managing payments."""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


# Template-based views
@login_required
def client_list(request):
    clients = Client.objects.all()
    return render(request, 'clients/client_list.html', {'clients': clients})


@login_required
def client_detail(request, pk):
    """View client details with financial stats and payment history."""
    client = get_object_or_404(Client, pk=pk)
    payments = client.payments.all()
    
    return render(request, 'clients/client_detail.html', {
        'client': client,
        'payments': payments,
    })


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


@login_required
def add_payment(request, pk):
    """Add a payment for a client."""
    if request.method == 'POST':
        client = get_object_or_404(Client, pk=pk)
        
        try:
            amount = request.POST.get('amount')
            date = request.POST.get('date')
            method = request.POST.get('method', 'CASH')
            reference = request.POST.get('reference', '')
            notes = request.POST.get('notes', '')
            
            Payment.objects.create(
                client=client,
                amount=amount,
                date=date,
                method=method,
                reference=reference,
                notes=notes,
            )
            messages.success(request, f'Payment of {amount} recorded successfully.')
        except Exception as e:
            messages.error(request, f'Error recording payment: {str(e)}')
        
        return redirect('client_detail', pk=pk)
    
    return redirect('client_detail', pk=pk)


@login_required
def delete_payment(request, pk, payment_id):
    """Delete a payment."""
    payment = get_object_or_404(Payment, pk=payment_id, client_id=pk)
    payment.delete()
    messages.success(request, 'Payment deleted successfully.')
    return redirect('client_detail', pk=pk)
