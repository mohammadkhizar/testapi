# Generated by Django 4.0.3 on 2022-08-16 14:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapi', '0003_user_role_alter_super_adminaccount_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='role',
        ),
    ]
