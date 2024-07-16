"""WhatsappMasivo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path
from django.conf.urls import url
from django.contrib import admin
from MessageSender.views import (index, login, data_upload, message_sending, check_message, send_messages,
                                 template_registry, upload_file, format_table, send_text_message,
                                 history, delete_template, format_history, get_message_base)
from ChatModule.views import (chat_module, whatsapp_webhook, chat_window, chat_list, api_image, get_pages,
                              update_seen, chat_lookup, contact_lookup)

urlpatterns = [
    path('', index),
    path('admin/', admin.site.urls),
    path('login/',login),
    path('data_upload/', data_upload),
    path('message_sending/', message_sending),
    path('check_message/', check_message),
    path('send_messages/', send_messages),
    path('register_template/',template_registry),
    path('chat/', chat_module),
    path('94710d4c-3596-4d40-82d0-385c360a63a9/', whatsapp_webhook),
    path('tyc/',login),
    path('chat_window/', chat_window),
    path('chat_list/', chat_list),
    path('image_api/', api_image),
    path('message_pages/', get_pages),
    path('update_seen/', update_seen),
    path('upload_file/', upload_file),
    path('format_table/', format_table),
    path('send_text_message/', send_text_message),
    path('history/', history),
    path('delete_template/', delete_template),
    path('format_history/', format_history),
    path('get_message_base/<str:template_name>', get_message_base,name='get_message_base'),
    path('contact_lookup/', contact_lookup),
    path('chat_lookup/', chat_lookup),
]
 