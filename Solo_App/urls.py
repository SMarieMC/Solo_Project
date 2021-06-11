from Solo_App import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('main', views.main),
    path('success', views.success),
    path('archive', views.archive),
    path('login-user', views.login_user),
    path('reg-user', views.register),
    path('logout', views.logout),
    path('add-comment', views.add_comment),
    path('feed', views.feed),
    path('users', views.users),
    path('like-comment/<int:id>', views.like_comment),
    path('delete/<int:id>', views.delete),
    path('edit-comment/<int:comment_id>', views.edit_comment),
    path('modify-comment', views.modify_comment),
    path('add-image', views.add_image),
]