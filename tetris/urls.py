from django.urls import path
from . import views

urlpatterns = [
    path('login', views.Login, name='login'),
    path('UserCreate', views.UserCreate, name='UserCreate'),
    path('tetris_result_submit', views.tetris_result_submit, name='tetris_result_submit'),
    path('ranking', views.ranking, name='ranking'),
    path('redisp_tetris', views.redisp_tetris, name='redisp_tetris'),
    path('HowToEnjoy', views.HowToEnjoy, name='HowToEnjoy'),
    path('Osirase', views.Osirase, name='Osirase'),
]