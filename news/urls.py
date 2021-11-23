from django.urls import path
from .views import PostCreateView, PostDeleteView, PostUpdateView, PostsList, PostDetail, PostsSearch

urlpatterns = [
    path('', PostsList.as_view(), name='news'),
    path('<int:pk>', PostDetail.as_view(), name='post'),
    path('search/', PostsSearch.as_view(), name='post'),
    path('add/', PostCreateView.as_view(), name='create'),
    path('edit/<int:pk>', PostUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', PostDeleteView.as_view(), name='delete'),
]
