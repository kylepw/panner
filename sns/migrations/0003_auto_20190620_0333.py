# Generated by Django 2.2.2 on 2019-06-20 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sns', '0002_auto_20190620_0111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='name',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
