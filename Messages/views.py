from django.http.response import HttpResponseRedirect
from Posts.templatetags.custom_filter import alert
from django.dispatch.dispatcher import receiver
from django.shortcuts import render
from django.contrib.auth.models import User
from .forms import SendMessage, SendPicture
from .models import Message, InboxAlert

# Create your views here.

def deport(req):
    return render(req, template_name='Messages/deport.html', context={})


def inbox(req, username):
    recipient = User.objects.get(username=username)
    new_message = SendMessage()
    new_picture = SendPicture()
    
    messages = Message.objects.filter(sender__in=[req.user, recipient], receiver__in=[req.user, recipient])

    InboxAlert.objects.filter(sender=recipient, receiver=req.user).update(alert=False)

    return render(req, template_name='Messages/inbox.html', context={'recipient':recipient, 'new_message':new_message, 'new_picture':new_picture, 'messages':messages})


def send_message(req, pk):
    recipient = User.objects.get(pk=pk)

    if req.method == 'POST':
        message = req.POST.get('message')
        if message != '':
            form = Message(message=message)
            form.sender = req.user
            form.receiver = recipient
            form.save()
    
    return HttpResponseRedirect(req.META['HTTP_REFERER'])


def send_picture(req, pk):
    recipient = User.objects.get(pk=pk)

    if req.method == 'POST':
        picture = req.FILES.get('picture')
        if picture is not None:
            form = Message(picture=picture)
            form.sender = req.user
            form.receiver = recipient
            form.save()
    
    return HttpResponseRedirect(req.META['HTTP_REFERER'])
