# Generated by Django 3.0.3 on 2020-05-30 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0005_auto_20200530_1210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manager_acc',
            name='passwd',
            field=models.CharField(max_length=200),
        ),
    ]
