# Generated by Django 3.0.3 on 2020-06-02 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_auto_20200601_1357'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='remarks',
            field=models.TextField(default='NA'),
        ),
    ]
