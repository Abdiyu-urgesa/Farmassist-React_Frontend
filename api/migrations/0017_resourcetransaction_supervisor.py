# Generated by Django 4.1.7 on 2023-06-25 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_resourcetransaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='resourcetransaction',
            name='supervisor',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
