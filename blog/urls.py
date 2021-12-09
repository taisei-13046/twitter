from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('create/', views.CreateTweetView.as_view(), name="create"),
    path('<int:pk>/', views.DetailTweetView.as_view(), name="detail"),
    path('<int:pk>/update/', views.UpdateTweetView.as_view(), name="update"),
    path('<int:pk>/delete/', views.DeleteTweetView.as_view(), name="delete"),
    path('<str:username>/following/', views.FollowingListView.as_view(), name="following"),
    path('<str:username>/follower/', views.FollowerListView.as_view(), name="follower"),
]
