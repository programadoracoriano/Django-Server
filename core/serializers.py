"""
This file has the serializers for api app models.
"""
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault, ImageField
from .models import *
from django.contrib.auth.models import User


#User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


#User profile serializer
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, many=False)
    class Meta:
        model = Profile
        fields = ('id', 'user', 'address', 'zip_code', 'location',
                  'phone', 'funds')

#Bike model serializer
class BikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bike
        fields = ('id', 'serie_number', 'date_bought', 'status', 'notes')

#Unlock packages model serializer
class UnlockPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnlockPackage
        fields = ('id', 'name', 'hours', 'price')


#Purchase serializer
class PurchaseSerializer(serializers.ModelSerializer):
    user    = UserSerializer(read_only=True, many=False)
    bike    = BikeSerializer(read_only=True, many=False)
    package = UnlockPackageSerializer(read_only=True, many=False)
    class Meta:
        model = Purchase
        fields = ('id', 'user', 'bike', 'package', 'date')

#Island Serializer
class IslandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Island
        fields = ('id', 'name', 'description_pt', 'description_en', 'image_url')
