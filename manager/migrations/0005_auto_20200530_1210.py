# Generated by Django 3.0.3 on 2020-05-30 12:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0004_account_passwd'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Account',
            new_name='Manager_Acc',
        ),
    ]
