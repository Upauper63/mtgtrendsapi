# Generated by Django 3.2.5 on 2021-07-10 19:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Scrape',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('started_at', models.DateTimeField(auto_now_add=True)),
                ('finished_at', models.DateTimeField(null=True)),
                ('is_finished', models.BooleanField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.IntegerField(db_index=True)),
                ('name', models.CharField(max_length=255)),
                ('diff_price_prev', models.IntegerField(null=True)),
                ('price_0', models.IntegerField(null=True)),
                ('price_1', models.IntegerField(null=True)),
                ('price_2', models.IntegerField(null=True)),
                ('price_3', models.IntegerField(null=True)),
                ('scrape_0', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='scrape_0', to='mtgtrendsapi.scrape')),
                ('scrape_1', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='scrape_1', to='mtgtrendsapi.scrape')),
                ('scrape_2', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='scrape_2', to='mtgtrendsapi.scrape')),
                ('scrape_3', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='scrape_3', to='mtgtrendsapi.scrape')),
            ],
        ),
    ]
