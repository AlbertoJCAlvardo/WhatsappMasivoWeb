from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from core.format import set_format,set_upper_format
from core.config import settings



def send_text_mesage(message, destiny, phone_number):
    phone_number_id = ""
    if phone_number == 'edilar':
        phone_number_id  = settings.PHONE_NUMBER
    if phone_number == 'redpotencia':
        phone_number_id  = settings.REDPOTENCIA_PHONE_NUMBER
    url = f'https://graph.facebook.com/v18.0/{phone_number_id}/messages'
    headers = {
        'Authorization': 'Bearer <ACCESS_TOKEN>',
        'Content-Type': 'application/json'
    }
    payload = {
        'messaging_product': 'whatsapp',
        'recipient_type': 'individual',
        'to': '<PHONE_NUMBER>',
        'type': 'text',
        'text': {
            'preview_url': False,
            'body': '<MESSAGE_CONTENT>'
        }
    }
    return 