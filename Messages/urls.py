from django.urls import path
from . import views



app_name = 'messages'

urlpatterns = [
    path('', views.deport, name='deport'),
    path('<username>/', views.inbox, name='inbox'),
    path('send-message/<pk>/', views.send_message, name='send_message'),
    path('send-picture/<pk>/', views.send_picture, name='send_picture'),
    ]