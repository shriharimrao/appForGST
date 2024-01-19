# Generated by Django 5.0.1 on 2024-01-19 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('quantity', models.IntegerField()),
                ('unit', models.CharField(max_length=20)),
                ('rate', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
