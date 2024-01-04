from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from core.utils import validate_session, validate_user
# Create your views here.

def initial_page(request):
    try:
        
        if request.method == 'GET':
            sesion_id = request.GET.get('sesion_id')
            user = request.GET.get('user')
            if validate_session(sesion_id) and validate_user(user):
                context = {}

                return HttpResponse(render_to_string('message_sender_index.html',
                                                     context=context))
        
    except Exception as e:

        return HttpResponseForbidden