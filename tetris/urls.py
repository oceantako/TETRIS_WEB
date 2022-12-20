from django.urls import path
from . import views

urlpatterns = [
    path('<str:login_name>/', views.login2, name='test'),
    path('<str:login_name>/test', views.login_test, name='login_test'),
    path('<str:login_name>/login', views.login_DB, name='login_DB'),
    path('login', views.Login, name='login'),
    path('UserCreate', views.UserCreate, name='UserCreate'),
]