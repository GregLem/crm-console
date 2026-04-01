from django.urls import path
from . import views

urlpatterns = [
    path('', views.lead_list, name='lead_list'),
    path('add/', views.add_lead, name='add_lead'),
]