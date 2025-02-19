from django.db.models import Count, F, Avg
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status
from rest_framework.response import Response

from apps.info_section_app.models import Favorite
from apps.title_app.models import Title, Rating
from apps.title_app.serializers import TitleListSerializer, TitleRatingSerializer, \
    TitleDetailSerializer, TitleInfoSerializer, RatingStatisticSerializer, FavoriteStatisticSerializer

from apps.title_app.filters import TitleFilter
from apps.title_app.permissions import RatingPermission


class TitleViewSet(viewsets.ModelViewSet):
    """ Manga-List """
    serializer_class = TitleListSerializer
    serializer_classes = {
        'retrieve': TitleDetailSerializer,
    }
    lookup_field = 'title_url'
    filterset_class = TitleFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['russian_name', 'english_name', 'alternative_names']
    ordering_fields = ['rating_count', 'english_name', 'date_created']

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_class)

    def get_queryset(self):
        return Title.objects.all().annotate(rating_count=Count('rate__star'),
                                            _average_rating=Avg('rate__star'),
                                            title_type_name=F('title_type__name'),
                                            adult_content_name=F('adult_content__name'),
                                            translator_status_name=F('translator_status__name')
                                            ).order_by('-rating_count')


class TitleInfoViewSet(viewsets.ModelViewSet):
    """ Info Section Manga """
    serializer_class = TitleInfoSerializer
    lookup_field = 'title_url'
    queryset = Title.objects.all()


class MyUserRatingView(viewsets.ModelViewSet):
    """ create/update Rating View """
    serializer_class = TitleRatingSerializer
    permission_classes = (RatingPermission,)
    queryset = Rating.objects.all()
    lookup_field = 'title_pk'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            user=self.request.user,
            title=kwargs.get('title_pk')
        )
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)


class RatingStatisticView(viewsets.ModelViewSet):
    """ Statistic Rating View """
    serializer_class = RatingStatisticSerializer
    lookup_field = 'title_pk'

    def get_queryset(self):
        title = self.kwargs['title_pk']
        filtering_by_title = Rating.objects.filter(title=title)
        rating_statistic = filtering_by_title.values('star').annotate(
            counting=Count('star'),
            percentage=Count('star')*100/len(filtering_by_title)
        )
        return rating_statistic


class FavoriteStatisticView(viewsets.ModelViewSet):
    """ Statistic Favorite View """
    serializer_class = FavoriteStatisticSerializer
    lookup_field = 'title_pk'

    def get_queryset(self):
        title = self.kwargs['title_pk']
        filtering_by_title = Favorite.objects.filter(title=title)
        favorite_statistic = filtering_by_title.values('folder').annotate(
            counting=Count('folder'),
            percentage=Count('folder') * 100 / len(filtering_by_title)
        )
        return favorite_statistic


