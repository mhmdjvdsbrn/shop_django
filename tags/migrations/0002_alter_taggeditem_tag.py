# Generated by Django 4.0.5 on 2022-07-04 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taggeditem',
            name='tag',
            field=models.SlugField(),
        ),
    ]
