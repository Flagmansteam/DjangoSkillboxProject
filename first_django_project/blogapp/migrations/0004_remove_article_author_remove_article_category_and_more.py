# Generated by Django 4.2 on 2023-10-01 22:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0003_rename_pubished_at_article_published_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='author',
        ),
        migrations.RemoveField(
            model_name='article',
            name='category',
        ),
        migrations.RemoveField(
            model_name='article',
            name='tags',
        ),
        migrations.DeleteModel(
            name='Author',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='Tags',
        ),
    ]