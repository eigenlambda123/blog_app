from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/edit', views.edit_post, name='edit_post'),
    path('post/<int:pk>/delete', views.delete_post, name='delete_post'),
    path('post/add/', views.add_post, name='add_post'),
]