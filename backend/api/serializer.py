import email
from enum import unique
from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from .models import Restaurant,Menu,Contact,UserProfile, Order, Reviews
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate
from rest_framework.request import Request
from api.models import LoginTracker


# from rest_framework_recursive.fields import RecursiveField


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'



# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username','first_name','last_name','email','is_staff','is_superuser','is_active')

class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

class ReviewSerializer(serializers.ModelSerializer):
    user = UserDataSerializer(many=False)
    restaurant = RestaurantSerializer(many=False)

    class Meta:
        model =  Reviews
        fields = '__all__'


class MenuSerializer(serializers.ModelSerializer):
    # children= RecursiveField(many = True)
    restaurant = RestaurantSerializer(many=False)

    class Meta:
        model = Menu
        fields = '__all__'

    # def create(self, validated_data):
    #     return Menu.objects.create(**validated_data)


class MenuSerializers(serializers.ModelSerializer):

    class Meta:
        model = Menu
        fields = '__all__'



class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


MIN_LENGTH = 5




class ProfileSerializer(serializers.ModelSerializer):
    # children= RecursiveField(many = True)
    user = UserSerializer(many=False)

    class Meta:
        model = UserProfile
        fields = '__all__'

#to update the data
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username','first_name','last_name','email')





class OrderSerializer(serializers.ModelSerializer):

    user = UserSerializer(many=False)

    class Meta:
        model =  Order
        fields = '__all__'


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only = True,
        min_length = MIN_LENGTH,
        error_messages = {
            "min_length" : f"Password must be longer than {MIN_LENGTH} characters."
        }
    )

    password2 = serializers.CharField(
        write_only = True,
        min_length = MIN_LENGTH,
        error_messages = {
            "min_length" : f"Password must be longer than {MIN_LENGTH} characters."
        }
    )
    first_name = serializers.CharField(max_length = 100)
    last_name = serializers.CharField(max_length = 100)
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    is_active = serializers.BooleanField(default=False)


    class Meta:
        model = User
        fields = "__all__"
        # extra_kwargs = {"first_name": {"error_messages": {"required": "Fill up the first name"}}}


    def validate(self, data):
        # raise serializers.ValidationError(str(data))
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'passworderror':"Password doesnot match"})
        return data
    

       
    
    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data['username'],
            email = validated_data['email'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],

        )

        user.set_password(validated_data['password'])
        user.is_active = False
        user.save()


        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        tracker_obj = LoginTracker.objects.get_or_create(username=data.get("username"))[0]
        is_valid = tracker_obj.valid_login()
        if not is_valid[0]:
            raise serializers.ValidationError(f'Tried more than 5 times. Try again in {is_valid[1]}')
        if user and user.is_active:
            return user
        tracker_obj.add_try()
        raise serializers.ValidationError('Incorrect Credentials Passed.')



     
    # class Meta:
    #     model = User
    #     fields = "__all__"
    #     extra_kwargs = {'password': {'write_only': True}}

    # def create(self, validated_data):
    #     user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

    #     return user

# class VerifyAccountSerializer(serializers.Serializer):
#     email = serializers.EmailField()

