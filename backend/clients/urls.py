from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'clients', views.ClientViewSet)
router.register(r'payments', views.PaymentViewSet)

urlpatterns = [
    # API routes
    path('', include(router.urls)),
]

# Template-based URL patterns (to be included in main urls.py)
template_urlpatterns = [
    path('clients/', views.client_list, name='client_list'),
    path('clients/add/', views.client_create, name='client_create'),
    path('clients/<int:pk>/', views.client_detail, name='client_detail'),
    path('clients/<int:pk>/edit/', views.client_edit, name='client_edit'),
    path('clients/<int:pk>/delete/', views.client_delete, name='client_delete'),
    path('clients/<int:pk>/payments/add/', views.add_payment, name='add_payment'),
    path('clients/<int:pk>/payments/<int:payment_id>/delete/', views.delete_payment, name='delete_payment'),
]
