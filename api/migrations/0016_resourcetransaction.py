# Generated by Django 4.1.7 on 2023-06-25 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_alter_post_posted_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResourceTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sold_recource', models.CharField(max_length=200, null=True)),
                ('amount', models.CharField(max_length=200, null=True)),
                ('buyer', models.CharField(max_length=200, null=True)),
                ('seller', models.CharField(max_length=200, null=True)),
                ('price_perKilo', models.CharField(max_length=200, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
    ]