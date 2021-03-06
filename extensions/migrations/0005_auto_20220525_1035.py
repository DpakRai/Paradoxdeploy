# Generated by Django 3.2 on 2022-05-25 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_useractivity_device'),
        ('extensions', '0004_remove_extension_developer_remove_extension_rating_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='extension',
            name='review',
        ),
        migrations.AddField(
            model_name='extension',
            name='reviews',
            field=models.ManyToManyField(related_name='extension_reviews', to='users.Review'),
        ),
    ]
