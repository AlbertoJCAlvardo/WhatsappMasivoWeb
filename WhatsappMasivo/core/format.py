import os
import csv
import string

from datetime import datetime

from django.conf import settings

date_format = "%d/%m/%Y"


def set_format(value):
    if value and type(value) is datetime:
        return "{}".format(value.strftime(date_format))

    return "{}".format(value) if value else ''


def set_upper_format(value):
    return "{}".format(value.upper()) if value else ''

