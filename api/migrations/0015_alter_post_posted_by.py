# Generated by Django 4.1.7 on 2023-06-12 19:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0014_rename_name_report_report_name_remove_post_f_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='posted_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
