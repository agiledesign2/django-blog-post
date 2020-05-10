# Generated by Django 2.0.7 on 2020-05-10 13:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import markdownx.models
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0002_auto_20150616_2121'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='Title')),
                ('slug', models.SlugField(max_length=255, unique_for_date='published_date')),
                ('content', markdownx.models.MarkdownxField()),
                ('description', models.TextField(help_text='Enter you description text here.', max_length=150, verbose_name='Description')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Created')),
                ('updated', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='Updated')),
                ('published', models.DateTimeField(blank=True, null=True, verbose_name='Published')),
                ('allow_comments', models.BooleanField(default=True)),
                ('status', models.SmallIntegerField(choices=[(1, 'Draft'), (2, 'Published')], verbose_name='State')),
                ('views_count', models.IntegerField(default=0, editable=False, verbose_name='View count')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='autors', to=settings.AUTH_USER_MODEL, verbose_name='Author')),
                ('category', models.ManyToManyField(related_name='Category', to='posts.Category')),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'ordering': ('-published',),
            },
        ),
    ]
