from django.urls import path
from . import views

urlpatterns = [
    path('', views.abikasse, name='abikasse'),
]

