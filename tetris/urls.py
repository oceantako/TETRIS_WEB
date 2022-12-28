from django.urls import path
from . import views

urlpatterns = [
    path('<str:login_name>/', views.login2, name='test'),
    path('<str:login_name>/test', views.login_test, name='login_test'),
    path('<str:login_name>/login', views.login_DB, name='login_DB'),
    path('login', views.Login, name='login'),
    path('UserCreate', views.UserCreate, name='UserCreate'),
    path('tetris_result_submit', views.tetris_result_submit, name='tetris_result_submit'),
    path('weekly_ranking', views.weekly_ranking, name='weekly_ranking'),
    path('monthly_ranking', views.monthly_ranking, name='monthly_ranking'),
    path('all_season_ranking', views.all_season_ranking, name='all_season_ranking'),
    path('submittest', views.submittest, name='submittest'),
]