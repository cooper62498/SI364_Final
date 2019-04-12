from django.urls import path
from . import views

urlpatterns = [
    path("", views.SkiHomeView.as_view(), name="ski_home"),
    path("mountains", views.SkiMountains.as_view(), name="main_state_mountain_list"),
    path("mountains/<str:state>", views.StateList.as_view(), name="state"),
    path(
        "mountains/<str:state>/<str:mountain>", views.Montain.as_view(), name="mountain"
    ),
    path(
        "mountains/<str:state>/<str:mountain>/comment",
        views.CommentCreateView.as_view(),
        name="comment_create",
    ),
    path(
        "comment/<int:pk>/delete",
        views.CommentDeleteView.as_view(),
        name="comment_delete",
    ),
    path(
        "mountains/<str:state>/<str:mountain>/favorite",
        views.AddFavoriteView.as_view(),
        name="mountain_favorite",
    ),
    path(
        "mountains/<str:state>/<str:mountain>/unfavorite",
        views.DeleteFavoriteView.as_view(),
        name="mountain_unfavorite",
    ),
    path("favorites", views.MyFavoriteView.as_view(), name="my_favorites"),
]
