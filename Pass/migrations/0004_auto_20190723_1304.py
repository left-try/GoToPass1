# Generated by Django 2.2.3 on 2019-07-23 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pass', '0003_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='cours',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='person',
            name='vk_id',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]