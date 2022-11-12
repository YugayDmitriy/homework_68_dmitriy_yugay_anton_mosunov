from django.urls import path
# from posts.views.posts import PostCreateView, PostLikeView, CommentCreateView, PostView, PostUpdateView, PostDeleteView
# from posts.views.base import PostsIndexView


urlpatterns = [
    # path('posts/<int:pk>/create/', PostCreateView.as_view(), name='create_post'),
    # path('posts/<int:pk>/like/', PostLikeView.as_view(), name='like'),
    # path('posts/<int:pk>/comment/', CommentCreateView.as_view(), name='comment'),
    path('', VacanciesIndexView.as_view(), name='index'),
    # path('post/<int:pk>', PostView.as_view(), name='post_detail'),
    # path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    # path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    # path('posts/<int:pk>/confirm-delete/', PostDeleteView.as_view(), name='confirm_delete'),

]