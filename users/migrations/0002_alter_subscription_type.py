# Generated by Django 4.0.2 on 2022-02-21 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='type',
            field=models.IntegerField(choices=[(1, 'basic'), (2, 'professional'), (3, 'business')], default=1),
        ),
    ]
