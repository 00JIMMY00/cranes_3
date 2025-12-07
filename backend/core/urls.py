"""
URL configuration for core project.
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from drivers.models import Driver, Loan
from cranes.models import Crane
from clients.models import Client
from drivers.urls import template_urlpatterns as driver_urls
from cranes.urls import template_urlpatterns as crane_urls
from clients.urls import template_urlpatterns as client_urls
from timesheets.urls import urlpatterns as timesheet_urls
from timesheets.models import TimeSheet
from reports.urls import urlpatterns as report_urls


@login_required
def dashboard(request):
    context = {
        'driver_count': Driver.objects.count(),
        'crane_count': Crane.objects.count(),
        'client_count': Client.objects.count(),
        'timesheet_count': TimeSheet.objects.count(),
        'loan_count': Loan.objects.count(),
    }
    return render(request, 'dashboard.html', context)


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


urlpatterns = [
    # Home
    path('', home, name='home'),
    
    # Dashboard
    path('dashboard/', dashboard, name='dashboard'),
    
    # Authentication
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Admin
    path('admin/', admin.site.urls),
    
    # API routes
    path('api/', include('drivers.urls')),
    path('api/', include('cranes.urls')),
    path('api/', include('clients.urls')),
]

# Add template-based URL patterns
urlpatterns += driver_urls
urlpatterns += crane_urls
urlpatterns += client_urls
urlpatterns += timesheet_urls
urlpatterns += report_urls
