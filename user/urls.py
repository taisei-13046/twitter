from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'user'

urlpatterns = [
    path('', views.SignUpView.as_view(), name="signup"),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('<str:username>', views.FollowIndexView.as_view(), name="follow_index"),
    path('<str:username>/follow/', views.follow_view, name="follow"),
    path('<str:username>/unfollow/', views.unfollow_view, name="unfollow"),
]
