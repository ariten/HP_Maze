
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('testjson', views.test_json_call, name='test_call'),
    path('registerteam', views.api_register_team, name='register_team'),
    path('teamselection', views.team_selection, name='team_selection'),
    path('userinput', views.api_user_input, name='user_input'),
    path('timeuntilstart', views.api_time_until_start, name='time_until_start'),
    path('sidechallenges', views.page_side_challenges, name='side_challenges'),
]

