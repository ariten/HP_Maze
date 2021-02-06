
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('testjson', views.test_json_call, name='test_call'),
    path('registerteam', views.register_team, name='register_team')
]

