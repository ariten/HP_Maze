
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
    path('submitsidechallenge', views.api_submit_side_challenge, name="submit_side_challenge"),
    path('getsidechallangehint', views.api_get_hint, name='get_hints'),
    path('getgamestartinfo', views.api_get_game_start_info, name='get_game_start_info'),
    path('adminextras', views.page_admin_extras, name='admin_extras'),
    path('adminendgame', views.api_admin_end_game, name='admin_end_game'),
]

