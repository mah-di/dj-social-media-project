from django.contrib import admin
from .models import Message, InboxAlert

# Register your models here.

admin.site.register(Message)
admin.site.register(InboxAlert)