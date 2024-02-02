from django.db import models

class UsersProfile(models.Model):
    user_name = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    user_type = models.CharField(max_length=10)
    
class Passenger(models.Model):
    user_profile = models.OneToOneField(UsersProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    phone_number = models.CharField(max_length=20)
    on_ride = models.BooleanField(default=False)

class Driver(models.Model):
    user_profile = models.OneToOneField(UsersProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    license_plate = models.CharField(max_length=20, null=True)
    color = models.CharField(max_length=50, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    availability = models.BooleanField(default=True)
    
    
class Service(models.Model):
    driver = models.ForeignKey('Driver', on_delete=models.CASCADE, null=True)
    passenger = models.ForeignKey('Passenger', on_delete=models.CASCADE)
    latitude_origin = models.DecimalField(max_digits=9, decimal_places=6)
    longitude_origin = models.DecimalField(max_digits=9, decimal_places=6)
    latitude_destination = models.DecimalField(max_digits=9, decimal_places=6)
    longitude_destination = models.DecimalField(max_digits=9, decimal_places=6)
    is_active = models.BooleanField(default=True)
    is_finished = models.BooleanField(default=False)
    is_canceled = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)