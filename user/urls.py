from django.urls import path

from . import views

app_name = 'user'
urlpatterns = [
	path('', views.IndexView.as_view(), name='index'),
	path('signup/', views.SignUpView.as_view(), name="signup"),
    path('home/', views.HomeView.as_view(), name="home"),
]

