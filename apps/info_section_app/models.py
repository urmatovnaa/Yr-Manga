from django.db import models

from multiselectfield import MultiSelectField

from apps.account_app.models import Account

from main.settings import AUTH_USER_MODEL

from apps.title_app.models import Title


CRITERION_CHOICES = (
        ('same genres', 'По жанрам'),
        ('same panache', 'По рисовке'),
        ('same plot', 'По сюжету'))


class SimilarTitle(models.Model):
    """ Model for Similar Titles """
    main_title = models.ForeignKey(Title, on_delete=models.CASCADE,
                                   verbose_name='Главный тайтл ', related_name='similar_titles')
    title = models.ForeignKey(Title, on_delete=models.SET_NULL,
                              verbose_name='Похожий тайтл', related_name='sim_title', null=True)
    criterion = MultiSelectField(max_length=25,
                                 choices=CRITERION_CHOICES,
                                 max_choices=2,
                                 verbose_name='Выбрать критерий схожести (макс. 2)')

    class Meta:
        verbose_name = 'Похожее'
        verbose_name_plural = 'Похожее'
        unique_together = (("main_title", "title"),)

    def __str__(self):
        return f'{self.title} - {self.main_title} - {self.criterion}'


class SimilarLike(models.Model):
    """ Likes for Similar Titles """
    similar = models.ForeignKey(SimilarTitle, models.CASCADE, related_name='likes')
    user = models.ForeignKey(AUTH_USER_MODEL, models.SET_NULL, null=True)


class SimilarDislike(models.Model):
    """ Dislikes for Similar Titles """
    similar = models.ForeignKey(SimilarTitle, models.CASCADE, related_name='dislikes')
    user = models.ForeignKey(AUTH_USER_MODEL, models.SET_NULL, null=True)


class RelatedTitle(models.Model):
    """ Model for Related Titles """
    RELATED_TYPE_CHOICES = (
        ('adaptation', 'Адаптация'),
        ('origin', 'Источник'),
        ('backstory', 'Предыстория'),
        ('continuation', 'Продолжение'),
        ('alternative history', 'Альтернативная история'),
        ('spin-off', 'Спин-офф'),
        ('crossover', 'Кроссовер'),
        ('color version', 'Цветная версия'),
        ('restart', 'Перезапуск'),
        ('another', 'Другое'),
    )

    user = models.ManyToManyField(Account,
                                  verbose_name='пользователи',
                                  related_name='related_title_owners')
    main_title = models.ForeignKey(Title, on_delete=models.CASCADE,
                                   verbose_name='Главный тайтл ', related_name='related_titles')
    title = models.ForeignKey(Title, on_delete=models.SET_NULL,
                              verbose_name='Связанный тайтл', related_name='rel_title', null=True)
    related_type = models.CharField(max_length=50,
                                    choices=RELATED_TYPE_CHOICES,
                                    verbose_name='Тип связи')

    class Meta:
        verbose_name = 'Связанное'
        verbose_name_plural = 'Связанное'
        unique_together = (("main_title", "title"),)

    def __str__(self):
        return f'{self.title} - {self.main_title} - {self.related_type}'


class Favorite(models.Model):
    """ Избранное """
    FOLDER_CHOICES = (
        ('Читаю', 'Читаю'),
        ('Прочитано', 'Прочитано'),
        ('Брошено', 'Брошено'),
        ('В планах', 'В планах'),
        ('Любимые', 'Любимые'),
    )
    user = models.ForeignKey(Account,
                             on_delete=models.CASCADE,
                             verbose_name='пользователь',
                             related_name='favorite_user')
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              verbose_name='тайтл',
                              related_name='manga_list')
    folder = models.CharField(max_length=255,
                              choices=FOLDER_CHOICES,
                              verbose_name='вкладка')

    class Meta:
        verbose_name = 'В списках'
        verbose_name_plural = 'В списках'
        unique_together = (("user", "title"),)

    def __str__(self):
        return f'{self.title} - {self.folder} - {self.user}'

