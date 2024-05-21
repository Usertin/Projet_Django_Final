from xml.etree.ElementInclude import include
from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='home'),
    path('create/', views.create_user, name='create_user'),
    path('index/', views.index, name='index'),
    path('profilepage/', views.profile_page, name='profile_page'),
    path('post/', views.post_list, name='post_list'),
    path('createPost/', views.create_post, name='create_post'),
    path('postDetail/<int:post_id>/', views.post_detail, name='post_detail'),
    path('updatePost/<int:post_id>/', views.update_post, name='update_post'),
    path('deletePost/<int:post_id>/', views.delete_post, name='delete_post'),
    path('postComment/<int:post_id>/', views.post_comment, name='post_comment'),
    path('addComment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('like-post/<int:post_id>/', views.like_post, name='like_post'),
    path('request-transport/<int:post_id>/', views.request_transport, name='request_transport'),
    path('transport-requests/<int:post_id>/', views.transport_requests, name='transport_requests'),
]