from rest_framework import serializers
from .models import *


class UsersProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersProfile
        fields = ['user_name', 'password', 'user_type']
        
class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['user_profile', 'name', 'phone_number', 'license_plate', 'color', 'latitude', 'longitude', 'availability']

class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = ['user_profile', 'name', 'latitude', 'longitude','phone_number', 'on_ride']
        
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id','latitude_origin','longitude_origin','latitude_destination','longitude_destination','is_active','is_finished','is_canceled','price','driver','passenger']
        
        