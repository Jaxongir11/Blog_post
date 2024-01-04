from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, add_comment, \
    PostUpdateView, PostDeleteView, CommentUpdateView, CommentDeleteView, \
    CategoryArchiveView, popular_posts,last_posts

app_name = 'post'

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('last/', last_posts, name='last-post'),
    path('popular/<str:period>/', popular_posts, name='popular_posts_with_period'),
    path('category/<str:category>/', CategoryArchiveView.as_view(), name='category-archive'),
    path('create/', PostCreateView.as_view(), name='post-create'),
    path('<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('<slug:slug>/add-comment/', add_comment, name='add-comment'),
    path('<slug:slug>/update-comment/<int:pk>/', CommentUpdateView.as_view(), name='update-comment'),
    path('<slug:slug>/comment-delete/<int:pk>/', CommentDeleteView.as_view(), name='delete-comment'),
]
