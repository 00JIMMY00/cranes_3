from django.urls import path
from . import views

urlpatterns = [
    # Single entry time sheets (legacy)
    path('timesheets/', views.timesheet_list, name='timesheet_list'),
    path('timesheets/add/', views.timesheet_create, name='timesheet_create'),
    path('timesheets/<int:pk>/edit/', views.timesheet_edit, name='timesheet_edit'),
    path('timesheets/<int:pk>/delete/', views.timesheet_delete, name='timesheet_delete'),
    path('timesheets/calculate/', views.timesheet_calculate, name='timesheet_calculate'),
    
    # Monthly time sheets (hard copy format)
    path('monthly-sheets/', views.monthly_sheet_list, name='monthly_sheet_list'),
    path('monthly-sheets/create/', views.monthly_sheet_create, name='monthly_sheet_create'),
    path('monthly-sheets/<int:pk>/', views.monthly_sheet_detail, name='monthly_sheet_detail'),
    path('monthly-sheets/<int:pk>/delete/', views.monthly_sheet_delete, name='monthly_sheet_delete'),
    path('monthly-sheets/<int:pk>/save/', views.monthly_sheet_save_all, name='monthly_sheet_save'),
    
    # AJAX endpoints
    path('daily-entry/<int:pk>/update/', views.daily_entry_update, name='daily_entry_update'),
    path('monthly-sheets/<int:pk>/add-shift/', views.add_shift_entry, name='add_shift_entry'),
    path('daily-entry/<int:pk>/delete/', views.delete_shift_entry, name='delete_shift_entry'),
]
