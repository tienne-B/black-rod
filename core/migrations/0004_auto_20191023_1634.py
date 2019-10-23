# Generated by Django 2.2.6 on 2019-10-23 16:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20191023_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='num_debaters',
            field=models.IntegerField(verbose_name='Debaters'),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='num_novice_debaters',
            field=models.IntegerField(verbose_name='Novice Debaters'),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='num_novice_teams',
            field=models.IntegerField(verbose_name='Novice Teams'),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='num_rounds',
            field=models.IntegerField(default=5, verbose_name='Rounds'),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='num_teams',
            field=models.IntegerField(verbose_name='Teams'),
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('debaters', models.ManyToManyField(to='core.Debater')),
                ('school', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='teams', to='core.School')),
            ],
        ),
    ]