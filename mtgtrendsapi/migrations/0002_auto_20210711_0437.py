# Generated by Django 3.2.5 on 2021-07-10 19:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mtgtrendsapi', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='item',
            table='items',
        ),
        migrations.AlterModelTable(
            name='scrape',
            table='scrapes',
        ),
    ]
