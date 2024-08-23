from celery import shared_task
from celery.signals import task_success
from .services import extract_invoice_data_service
import requests

@shared_task
def process_pdf_task(pdf_file):
    print("data extraction started")
    result = extract_invoice_data_service(pdf_file)
    return result

@task_success.connect(sender=process_pdf_task)
def send_data_to_node_server(sender , result , **kwargs):
    node_server_url = 'http://192.168.31.60:8080/api/core/data/addExtractedData'

    try:
        task_id = sender.request.id

        payload = {
            'data': {
                'status': 200,
                'message': 'Data extracted Successfully !!',
                'result': result,
                'task_id': task_id
            }
        }

        response = requests.post(node_server_url , json=payload)
        response.raise_for_status()
        print(f"Successfully sent the result to the Node.js Server: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send result to the Node.js server: {str(e)}")