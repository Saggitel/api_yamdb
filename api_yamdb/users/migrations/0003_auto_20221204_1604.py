# Generated by Django 2.2.16 on 2022-12-04 13:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20221203_1220'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('role',)},
        ),
    ]