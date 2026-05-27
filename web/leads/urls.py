from django.urls import path
from . import views

urlpatterns = [
    path('', views.lead_list, name='lead_list'),
    path('add/', views.add_lead, name='add_lead'),
    path('kanban/', views.kanban_board, name='kanban_board'),
    path('analytics/', views.analytics_dashboard, name='analytics_dashboard'),
    path('api/update-status/', views.update_lead_status, name='update_lead_status'),
    path('export/excel/', views.export_leads_excel, name='export_leads_excel'),
]