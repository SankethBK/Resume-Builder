# Generated by Django 3.0.5 on 2020-04-26 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_jobinvites'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobinvites',
            name='applicants',
            field=models.TextField(default='^'),
        ),
    ]
