from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .services import extract_invoice_data_service

@api_view(['POST'])
def extract_data_from_invoice(request):
    pdf_url = request.data.get('pdf_url')
    if not pdf_url:
        return JsonResponse({'error':'PDF Url is Required'}, status=400)
    
    try:
        data_output = extract_invoice_data_service(pdf_url)
        return JsonResponse(data_output , safe=False)
    
    except Exception as e:
        return JsonResponse({'error': str(e)} , status=500)
    
