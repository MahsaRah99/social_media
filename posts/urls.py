from django.urls import path
from . import views

app_name = "posts"
urlpatterns = [
    path("home/", views.HomeView.as_view(), name="home"),
    path(
        "post/<uuid:post_id>/<slug:post_slug>/",
        views.PostDetailView.as_view(),
        name="post_detail",
    ),
    path(
        "post/delete/<uuid:post_id>/", views.PostDeleteView.as_view(), name="post_delete"
    ),
    path(
        "post/update/<uuid:post_id>/", views.PostUpdateView.as_view(), name="post_update"
    ),
    path("post/create/", views.PostCreateView.as_view(), name="post_create"),
    path(
        "reply/<uuid:post_id>/<uuid:comment_id>/",
        views.PostAddReplyView.as_view(),
        name="add_reply",
    ),
    path("like/<uuid:post_id>/", views.PostLikeView.as_view(), name="post_like"),
]
