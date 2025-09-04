from django.urls import path
from . import views
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    BlogSearchListView,
    BlogAjaxSearchView,
)

urlpatterns = [
    path("", PostListView.as_view(), name="blog-home"),
    path("user/<str:username>/", UserPostListView.as_view(), name="user-posts"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("post/new/", PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
    path("blog_search_list/", BlogSearchListView.as_view(), name="blog-search-list"),
    path("ajax/search/", BlogAjaxSearchView.as_view(), name='ajax-search'),
    path("about/", views.about, name="blog-about"),
]
