# Generated by Django 3.0.4 on 2020-04-18 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20200418_1228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='followers',
            field=models.TextField(default='', verbose_name={'required': False}),
        ),
        migrations.AlterField(
            model_name='profile',
            name='following',
            field=models.TextField(default='', verbose_name={'required': False}),
        ),
    ]