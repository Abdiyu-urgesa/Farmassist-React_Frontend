# Generated by Django 4.1.7 on 2023-03-22 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_resource_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resource',
            name='user',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='resource',
            field=models.ManyToManyField(to='api.resource'),
        ),
    ]
