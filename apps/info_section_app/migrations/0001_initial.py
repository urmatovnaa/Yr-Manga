# Generated by Django 4.1.1 on 2023-05-29 12:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('title_app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SimilarTitle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criterion', multiselectfield.db.fields.MultiSelectField(choices=[('same genres', 'По жанрам'), ('same panache', 'По рисовке'), ('same plot', 'По сюжету')], max_length=25, verbose_name='Выбрать критерий схожести (макс. 2)')),
                ('main_title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='similar_titles', to='title_app.title', verbose_name='Главный тайтл ')),
                ('title', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sim_title', to='title_app.title', verbose_name='Похожий тайтл')),
            ],
            options={
                'verbose_name': 'Похожее',
                'verbose_name_plural': 'Похожее',
                'unique_together': {('main_title', 'title')},
            },
        ),
        migrations.CreateModel(
            name='SimilarLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('similar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='info_section_app.similartitle')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SimilarDislike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('similar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dislikes', to='info_section_app.similartitle')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RelatedTitle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('related_type', models.CharField(choices=[('adaptation', 'Адаптация'), ('origin', 'Источник'), ('backstory', 'Предыстория'), ('continuation', 'Продолжение'), ('alternative history', 'Альтернативная история'), ('spin-off', 'Спин-офф'), ('crossover', 'Кроссовер'), ('color version', 'Цветная версия'), ('restart', 'Перезапуск'), ('another', 'Другое')], max_length=50, verbose_name='Тип связи')),
                ('main_title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_titles', to='title_app.title', verbose_name='Главный тайтл ')),
                ('title', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rel_title', to='title_app.title', verbose_name='Связанный тайтл')),
                ('user', models.ManyToManyField(related_name='related_title_owners', to=settings.AUTH_USER_MODEL, verbose_name='пользователи')),
            ],
            options={
                'verbose_name': 'Связанное',
                'verbose_name_plural': 'Связанное',
                'unique_together': {('main_title', 'title')},
            },
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('folder', models.CharField(choices=[('Читаю', 'Читаю'), ('Прочитано', 'Прочитано'), ('Брошено', 'Брошено'), ('В планах', 'В планах'), ('Любимые', 'Любимые')], max_length=255, verbose_name='вкладка')),
                ('title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='manga_list', to='title_app.title', verbose_name='тайтл')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_user', to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'В списках',
                'verbose_name_plural': 'В списках',
                'unique_together': {('user', 'title')},
            },
        ),
    ]
