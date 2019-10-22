# Generated by Django 2.2.6 on 2019-10-22 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='included_in_oty',
            field=models.BooleanField(default=True, verbose_name='Included in OTY'),
        ),
        migrations.AlterField(
            model_name='school',
            name='name',
            field=models.CharField(max_length=64, unique=True),
        ),
    ]
