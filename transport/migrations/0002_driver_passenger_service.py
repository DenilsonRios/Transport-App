# Generated by Django 5.0.1 on 2024-01-29 23:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transport', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=20)),
                ('license_plate', models.CharField(max_length=20)),
                ('color', models.CharField(max_length=50)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('availability', models.BooleanField(default=True)),
                ('user_profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='transport.usersprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Passenger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('phone_number', models.CharField(max_length=20)),
                ('on_ride', models.BooleanField(default=False)),
                ('user_profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='transport.usersprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude_origin', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude_origin', models.DecimalField(decimal_places=6, max_digits=9)),
                ('latitude_destination', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude_destination', models.DecimalField(decimal_places=6, max_digits=9)),
                ('is_active', models.BooleanField(default=True)),
                ('is_finished', models.BooleanField(default=False)),
                ('is_canceled', models.BooleanField(default=False)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transport.driver')),
                ('passenger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transport.passenger')),
            ],
        ),
    ]
