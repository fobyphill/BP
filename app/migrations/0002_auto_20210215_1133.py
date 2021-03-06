# Generated by Django 3.1.6 on 2021-02-15 08:33

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatusTransfer',
            fields=[
                ('id', models.CharField(max_length=1, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterField(
            model_name='event',
            name='correlation_id',
            field=models.UUIDField(default=uuid.UUID('1293aff4-36ab-4c05-be64-21e53d9992df'), unique=True),
        ),
        migrations.AddField(
            model_name='transfer',
            name='status',
            field=models.ForeignKey(default='n', on_delete=django.db.models.deletion.DO_NOTHING, to='app.statustransfer'),
        ),
    ]
