# Generated by Django 5.0.1 on 2024-01-19 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gstin', models.CharField(blank=True, max_length=15, null=True, unique=True)),
            ],
        ),
    ]
