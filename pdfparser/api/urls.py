from django.urls import path
from .views import extract_data_from_invoice

urlpatterns = [
    path('extract/', extract_data_from_invoice, name='extract_data_from_invoice')
]