from django.urls import path
from apps.title_app.views import TitleViewSet, MyUserRatingView, TitleInfoViewSet, \
    RatingStatisticView

urlpatterns = [
    path('manga-list/', TitleViewSet.as_view({'get': 'list'})),
    path('<str:title_url>/', TitleViewSet.as_view(
        {'get': 'retrieve'}
    )),
    path('<str:title_url>/info', TitleInfoViewSet.as_view({'get': 'retrieve'})),
    path('<int:title_pk>/rating/create', MyUserRatingView.as_view({'post': 'create'})),
    path('<int:title_pk>/rating/statistic', RatingStatisticView.as_view({'get': 'list'})),

    # path('<int:rest_pk>/review/create/', ReviewView.as_view({'get': 'list', 'post': 'create'})),
]
