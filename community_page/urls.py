from django.urls import path
from . import views

urlpatterns = [
    # the community home page
    path('', views.index, name='community_home'),
    # the create post page
    path('create/', views.create_post, name='create_post'),
    # the like post page
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    # the add comment page
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
    # the delete post page
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
    # the delete comment page
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    # post workout from generator to community
    path('post-workout/', views.post_workout_to_community, name='post_workout_to_community'),
]
