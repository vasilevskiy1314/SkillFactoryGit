from django.urls import path
from .views import PostsList, PostDetailView, PostSearch, PostCreateView, PostUpdateView, PostDeleteView

urlpatterns = [
    path('', PostsList.as_view()),
    path('<int:pk>', PostDetailView.as_view(), name='post_detail'),
    path('search/', PostSearch.as_view(), name='post_search'),
    path('add/', PostCreateView.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
]