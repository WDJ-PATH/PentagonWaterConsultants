# Generated by Django 3.0.3 on 2020-06-01 13:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_auto_20200531_2226'),
    ]

    operations = [
        migrations.AddField(
            model_name='pent_user',
            name='latesttestdate',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
