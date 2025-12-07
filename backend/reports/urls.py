from django.urls import path
from . import views

urlpatterns = [
    path('reports/', views.reports_dashboard, name='reports_dashboard'),
    path('reports/invoice/', views.generate_invoice, name='generate_invoice'),
    path('reports/wage-slip/', views.generate_wage_slip, name='generate_wage_slip'),
]
