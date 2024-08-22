from celery import shared_task
from celery.signals import task_success
from .services import extract_invoice_data_service
import requests

@shared_task
def process_pdf_task(pdf_url):
    print("data extraction started")
    result = extract_invoice_data_service(pdf_url)
    return result

@task_success.connect(sender=process_pdf_task)
def send_data_to_node_server(sender , result , **kwargs):
    node_server_url = 'http://your-node-server.com/api/receive-data'

    try:
        response = requests.post(node_server_url , json=result)
        response.raise_for_status()
        print(f"Successfully sent the result to the Node.js Server: {response.json()}")
    except requests.exceptions.Requestexception as e:
        print(f"Failed to send result to the Node.js server: {str(e)}")