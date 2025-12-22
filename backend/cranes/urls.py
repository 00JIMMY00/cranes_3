from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'cranes', views.CraneViewSet)

urlpatterns = [
    # API routes
    path('', include(router.urls)),
]

# Template-based URL patterns (to be included in main urls.py)
template_urlpatterns = [
    path('cranes/', views.crane_list, name='crane_list'),
    path('cranes/<int:pk>/', views.crane_detail, name='crane_detail'),
    path('cranes/add/', views.crane_create, name='crane_create'),
    path('cranes/<int:pk>/edit/', views.crane_edit, name='crane_edit'),
    path('cranes/<int:pk>/delete/', views.crane_delete, name='crane_delete'),
]
