# Generated by Django 4.2.4 on 2023-08-07 21:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('creator', '0002_alter_user_managers_remove_user_username'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='usercampaign',
            unique_together={('user', 'campaign')},
        ),
    ]
