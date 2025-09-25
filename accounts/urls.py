from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [


    path('',  views.my_login, name="my_login"),
    path('register', views.register, name="register"),
    # path('my_login', views.my_login, name="my_login"),
    path('dashboard', views.dashboard, name="dashboard"),

    # path('user_logout', views.user_logout, name="user_logout"),

]

'''
    path("login/", auth_views.LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    path("", views.home, name="home"),
    '''

