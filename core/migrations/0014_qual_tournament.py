# Generated by Django 2.2.6 on 2019-10-26 19:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20191026_1739'),
    ]

    operations = [
        migrations.AddField(
            model_name='qual',
            name='tournament',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quals', to='core.Tournament'),
        ),
    ]
