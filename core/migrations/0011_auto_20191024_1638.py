# Generated by Django 2.2.6 on 2019-10-24 16:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20191024_1437'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='coty',
            options={'ordering': ('place',)},
        ),
        migrations.AlterModelOptions(
            name='noty',
            options={'ordering': ('place',)},
        ),
        migrations.AlterModelOptions(
            name='soty',
            options={'ordering': ('place',)},
        ),
        migrations.AlterModelOptions(
            name='toty',
            options={'ordering': ('place',)},
        ),
        migrations.AlterField(
            model_name='qual',
            name='qual_type',
            field=models.IntegerField(choices=[(1, 'Brandeis IV'), (2, 'Yale IV'), (3, 'NorthAms'), (4, 'Expansion'), (5, 'Worlds'), (6, 'NAUDC')], default=5),
        ),
        migrations.CreateModel(
            name='COTYDebater',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.FloatField(default=0)),
                ('season', models.CharField(choices=[('2000', '2000-2001'), ('2001', '2001-2002'), ('2002', '2002-2003'), ('2003', '2003-2004'), ('2004', '2004-2005'), ('2005', '2005-2006'), ('2006', '2006-2007'), ('2007', '2007-2008'), ('2008', '2008-2009'), ('2009', '2009-2010'), ('2010', '2010-2011'), ('2011', '2011-2012'), ('2012', '2012-2013'), ('2013', '2013-2014'), ('2014', '2014-2015'), ('2015', '2015-2016'), ('2016', '2016-2017'), ('2017', '2017-2018'), ('2018', '2018-2019'), ('2019', '2019-2020'), ('2020', '2020-2021'), ('2021', '2021-2022')], default='2018', max_length=16)),
                ('debater', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coty_debater', to='core.Debater')),
            ],
        ),
    ]
