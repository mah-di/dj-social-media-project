from django.db.models.fields import IntegerField
from django.forms import ModelForm
from django.forms.fields import CharField, ImageField
from django.forms.widgets import HiddenInput
from .models import Message


class SendMessage(ModelForm):
    message = CharField(required=True)
    class Meta:
        model = Message
        fields = ('message',)


class SendPicture(ModelForm):
    picture = ImageField(required=True)
    class Meta:
        model = Message
        fields = ('picture',)


class Share(ModelForm):
    attachment = IntegerField(HiddenInput(attrs={'hidden':True}))
    class Meta:
        model = Message
        fields = ('attachment',)