from django.urls import path
from .views import *

urlpatterns = [
    path('accounts', UserView.as_view(), name='user_view'),
    path('accounts/login', UserLoginView.as_view(), name='user_login'),
    path('me', UserDetailView.as_view(), name='user_detail'),
    path('blog', PostView.as_view(), name='post_view'),
    path('blog/<int:id>', PostDetailView.as_view(), name='post_detail'),
    path('like/<int:blog_id>', LikeView.as_view(), name='like_view'),

]
