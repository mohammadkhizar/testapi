# Generated by Django 4.0.3 on 2022-08-16 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapi', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=255)),
                ('alias', models.CharField(default='', max_length=255)),
                ('email', models.EmailField(default='', max_length=255)),
                ('password', models.TextField(default='', max_length=255)),
            ],
        ),
    ]
