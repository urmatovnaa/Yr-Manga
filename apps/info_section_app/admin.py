from django.contrib import admin

from django.contrib.admin.options import TabularInline

from apps.info_section_app.models import SimilarLike, SimilarDislike, SimilarTitle, \
    Favorite, RelatedTitle


class SimilarLikeAdminInLine(TabularInline):
    extra = 1
    model = SimilarLike


class SimilarDislikeAdminInline(TabularInline):
    extra = 1
    model = SimilarDislike


@admin.register(SimilarTitle)
class RestaurantModelAdmin(admin.ModelAdmin):
    inlines = (SimilarDislikeAdminInline, SimilarLikeAdminInLine)


admin.site.register(Favorite)
admin.site.register(RelatedTitle)



