# Generated by Django 2.2.16 on 2022-12-03 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_auto_20221203_1458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='description',
            field=models.TextField(null=True, verbose_name='Описание'),
        ),
    ]