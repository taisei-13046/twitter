from django.urls import path

from . import views

app_name = 'user'
urlpatterns = [
    path('', views.SignUpView.as_view(), name="signup"),
    path('home/', views.HomeView.as_view(), name="home"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
]
