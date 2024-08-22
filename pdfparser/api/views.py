from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
# from .services import extract_invoice_data_service
from .tasks import process_pdf_task

@api_view(['POST'])
def extract_data_from_invoice(request):
    pdf_url = request.data.get('pdf_url')
    if not pdf_url:
        return JsonResponse({'error':'PDF Url is Required'}, status=400)
    
    try:
        print('pdf url : =======> ' , pdf_url)
        task  = process_pdf_task.delay(pdf_url)
        return JsonResponse({'task_id': task.id} , status=202)
    
    except Exception as e:
        return JsonResponse({'error': str(e)} , status=500)
    
