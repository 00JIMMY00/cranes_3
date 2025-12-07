from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'drivers', views.DriverViewSet)
router.register(r'loans', views.LoanViewSet)

urlpatterns = [
    # API routes
    path('', include(router.urls)),
]

# Template-based URL patterns (to be included in main urls.py)
template_urlpatterns = [
    # Drivers
    path('drivers/', views.driver_list, name='driver_list'),
    path('drivers/add/', views.driver_create, name='driver_create'),
    path('drivers/<int:pk>/', views.driver_detail, name='driver_detail'),
    path('drivers/<int:pk>/edit/', views.driver_edit, name='driver_edit'),
    path('drivers/<int:pk>/delete/', views.driver_delete, name='driver_delete'),
    path('drivers/<int:driver_id>/add-loan/', views.loan_create, name='driver_add_loan'),
    
    # Loans
    path('loans/', views.loan_list, name='loan_list'),
    path('loans/add/', views.loan_create, name='loan_create'),
    path('loans/<int:pk>/edit/', views.loan_edit, name='loan_edit'),
    path('loans/<int:pk>/delete/', views.loan_delete, name='loan_delete'),
]
