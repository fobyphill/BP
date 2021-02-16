# Generated by Django 3.1.6 on 2021-02-16 08:59

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20210215_1645'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpaininformation',
            name='type',
            field=models.CharField(default='INDIVIDUAL', max_length=10),
        ),
        migrations.AlterField(
            model_name='event',
            name='correlation_id',
            field=models.UUIDField(default=uuid.UUID('ac5f55f3-c7a2-409b-852c-59c78c4972ec'), unique=True),
        ),
        migrations.AlterField(
            model_name='userpaininformation',
            name='ogrn',
            field=models.CharField(max_length=15, null=True),
        ),
    ]
