# Generated by Django 3.2 on 2022-07-22 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AI', '0015_alter_basedevice_reviews'),
    ]

    operations = [
        migrations.AddField(
            model_name='basedevice',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
