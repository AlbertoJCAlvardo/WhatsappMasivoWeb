from django.core.management.base import BaseCommand
from django.utils import timezone
from db.utils import DatabaseManager


class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
       dm = DatabaseManager('sistemas')
       dm.insert_message_response({'origin':'5215574078980',
                                   'destiny':'5215642237735'})
