from django.contrib.auth.models import User
from django.urls import path
from .views import PostCreateView, PostDeleteView, PostUpdateView, PostsList, PostDetail, PostsSearch, ProfileUpdateView
from .views import upgrade_me
from .views import SubscribeView
from .views import PostLimitView
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', PostsList.as_view(), name='news'),
    path('<int:pk>', PostDetail.as_view(), name='post'),
    path('search/', PostsSearch.as_view(), name='search'),
    path('add/', PostCreateView.as_view(), name='create'),
    path('add/limit/', PostLimitView.as_view()),
    path('edit/<int:pk>', PostUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', PostDeleteView.as_view(), name='delete'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('profile/', ProfileUpdateView.as_view(model=User), name='profile'),
    path('subscribe/', SubscribeView.as_view(), name='subscribe'),
    ]
