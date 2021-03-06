# Generated by Django 3.0.8 on 2020-08-03 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TechnicalAnalysis', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockLastUpdate',
            fields=[
                ('StockName', models.TextField()),
                ('StockSymbol', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('UpdateDate', models.DateField(blank=True, default=None)),
            ],
            options={
                'db_table': 'StockLastUpdate',
            },
        ),
    ]
