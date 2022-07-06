# Generated by Django 4.0.5 on 2022-07-04 17:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_videoproduct_video_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='videoproduct',
            name='video_product',
        ),
        migrations.AlterField(
            model_name='product',
            name='videos',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='shop.videoproduct'),
        ),
    ]
