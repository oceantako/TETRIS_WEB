# Generated by Django 3.0.2 on 2022-12-30 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tetris', '0003_auto_20221229_1748'),
    ]

    operations = [
        migrations.CreateModel(
            name='RankSelecter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('underblocks', models.IntegerField()),
                ('rank', models.CharField(max_length=20)),
                ('syougou', models.CharField(max_length=20)),
            ],
        ),
    ]
