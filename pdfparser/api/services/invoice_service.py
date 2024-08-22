import easyocr
import re
import requests
from pdf2image import convert_from_bytes
from io import BytesIO
import numpy as np

def extract_invoice_data_service(pdf_url):
    print("===========================>>>>>>>>>>>" , pdf_url)
    try:
        file_id = pdf_url.split('/')[5]
        direct_download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
        # Download the PDF file
        response = requests.get(direct_download_url)
        response.raise_for_status()
        
        # Convert PDF to images
        pdf_images = convert_from_bytes(response.content)

        # Initialize EasyOCR reader
        reader = easyocr.Reader(['en'], gpu=False)

        # Initialize the data output structure
        data_output = []

        for page_num, img in enumerate(pdf_images):
            # Convert the PIL image to a numpy array
            img_array = np.array(img)
            
            results = reader.readtext(
                img_array,
                paragraph=True,
                x_ths=0.3
            )
            
            page_data = {
                'page_number': page_num + 1,
                'InvoiceNumber': {
                    'text': '',
                    'position': []
                },
                'OrderID': {
                    'text': '',
                    'position': []
                },
                'InvoiceDate': {
                    'text': '',
                    'position': []
                },
                'GSTIN': {
                    'text': '',
                    'position': []
                },
                'IGST': {
                    'percent': '',
                    'amount': '',
                    'position': []
                },
                'TotalAmount': {
                    'text': '',
                    'position': []
                }
            }

            # Extract and store positions along with the text
            for result in results:
                bbox, text = result[0], result[1]
                
                if 'Original Invoice Number' or 'Invoice Number' in text:
                    match = re.search(r'Original Invoice Number\s*([^\s]+)', text)
                    if match:
                        page_data['InvoiceNumber']['text'] = match.group(1).strip()
                        page_data['InvoiceNumber']['position'] = bbox
                
                elif 'Order ID:' in text:
                    match = re.search(r'Order ID:\s*([^\s]+)', text)
                    if match:
                        page_data['OrderID']['text'] = match.group(1).strip()
                        page_data['OrderID']['position'] = bbox
                
                elif 'Invoice Date:' in text:
                    match = re.search(r'Invoice Date:\s*(\d{2}-\d{2}-\d{4})', text)
                    if match:
                        page_data['InvoiceDate']['text'] = match.group(1).strip()
                        page_data['InvoiceDate']['position'] = bbox
                
                elif 'GSTIN' in text:
                    match = re.search(r'GSTIN\s*[:\-]?\s*([0-9A-Z]{15})', text)
                    if match:
                        page_data['GSTIN']['text'] = match.group(1).strip()
                        page_data['GSTIN']['position'] = bbox
                
                elif 'IGST:' in text:
                    match = re.search(r'IGST\s*[:\-]?\s*([\d.]+)%?\s*([\d.,]+)?', text)
                    if match:
                        page_data['IGST']['percent'] = match.group(1).strip() if match.group(1) else ''
                        page_data['IGST']['amount'] = match.group(2).strip() if match.group(2) else ''
                        page_data['IGST']['position'] = bbox
                
                elif 'Grand Total' in text or 'Total' in text:
                    match = re.search(r'Grand Total\s*([\d.,]+)|Total\s*([\d.,]+)', text)
                    if match:
                        page_data['TotalAmount']['text'] = match.group(1) if match.group(1) else match.group(2)
                        page_data['TotalAmount']['position'] = bbox

            data_output.append(page_data)

        return data_output

    except requests.RequestException as e:
        raise Exception(f'Failed to download file: {str(e)}')
    except Exception as e:
        raise Exception(f'Error processing file: {str(e)}')
