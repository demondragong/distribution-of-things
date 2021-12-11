from . import views
from django.urls import path

urlpatterns = [
    path('', views.PostListView.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
]