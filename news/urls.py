from django.contrib.auth.models import User
from django.urls import path
from .views import PostCreateView, PostDeleteView, PostUpdateView, PostsList, PostDetail, PostsSearch, ProfileUpdateView
from .views import upgrade_me

urlpatterns = [
    path('', PostsList.as_view(), name='news'),
    path('<int:pk>', PostDetail.as_view(), name='post'),
    path('search/', PostsSearch.as_view(), name='add'),
    path('add/', PostCreateView.as_view(), name='create'),
    path('edit/<int:pk>', PostUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', PostDeleteView.as_view(), name='delete'),
    path('upgrade/', upgrade_me, name = 'upgrade'),
    path('profile/', ProfileUpdateView.as_view(model=User), name='profile'),
]