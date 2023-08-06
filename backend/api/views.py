import base64
from cProfile import Profile
from email import message
import logging
from math import perm
import random
import traceback
from urllib import response
from django.conf import settings
from django.shortcuts import get_object_or_404, render
from .serializer import OrderSerializer, RestaurantSerializer, MenuSerializer, ContactSerializer, UserProfileSerializer, ReviewSerializer, UserDataSerializer
from rest_framework.generics import ListAPIView
from .models import Restaurant, Menu, UserProfile, Order, Reviews, LoginTracker
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework.generics import ListAPIView
from knox.models import AuthToken
from .serializer import UserSerializer, RegisterSerializer, LoginSerializer, ProfileSerializer, MenuSerializers
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework import status
from django.http import JsonResponse, HttpRequest
from rest_framework import serializers
from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from django.core.mail import send_mail
import json
from rest_framework.authtoken.models import Token
from cryptography.fernet import Fernet
from rest_framework.views import APIView 
from django.conf import settings
from django.shortcuts import redirect
from operator import itemgetter

@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'List': '/restaurant-list',
        'Detail View': '/restaurant-detail/<str:pk>/',
        'Create' : '/restaurant-create/',
        'Update' : '/restaurant-update/<str:pk>/',
        'Delete' : '/restaurant-delete/<str:pk>/',

    }

    return Response(api_urls)

@api_view(['GET'])
def restaurantList(request):
    restaurants = Restaurant.objects.all()
    serializer = RestaurantSerializer(restaurants, many= True)
    return Response(serializer.data)



@api_view(['GET'])
def restaurantDetail(request, pk):
    restaurants = Restaurant.objects.get(id = pk)
    serializer = RestaurantSerializer(restaurants, many= False)
    return Response(serializer.data)


@api_view(['POST'])
def restaurantCreate(request):
    serializer = RestaurantSerializer(data = request.data)

    if serializer.is_valid():
        serializer.save()

    
    data={
        "message":"Added Successfully",
        "data": serializer.data,
    }
    return Response(data)

    
    # return Response({"status": "success", "data": serializer.data, status=status.HTTP_200_OK})
    # return JsonResponse(data, status=status.HTTP_201_CREATED)



@api_view(['POST'])
def restaurantUpdate(request,pk):
    # restaurants = Restaurant.objects.get(id = pk)
    restaurants = get_object_or_404(Restaurant, id=pk)
    serializer = RestaurantSerializer(instance=restaurants, data = request.data)
    print(request.data)

    if serializer.is_valid():
        serializer.save()
        data={
            "message":"Updated Successfully",
            "data": serializer.data,
        }
    else:
        data={
            "message":"Error"
        }
        return Response(data,status=500)
        
    return Response(data)


@api_view(['DELETE'])
def restaurantDelete(request,pk):
    restaurants = Restaurant.objects.get(id = pk)
    restaurants.delete()

    return Response('Item successfully Deleted')

# class UserListView(ListAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [IsAdminUser]

# class UserList(ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer




# Register API
class RegisterAPI(generics.GenericAPIView):
  
    serializer_class = RegisterSerializer
    
    def post(self, request, *args, **kwargs):
        myuser = request.data
        serializer = self.get_serializer(data=myuser)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        # user_data = serializer.data
        auth_token = AuthToken.objects.create(user)
        token = auth_token[0].digest
        print("Token-->",token)
        subject = "Your email needs to be verified"
        message = f'Thank you for registering, please click on the link to verify email http://127.0.0.1:8000/api/verify/{token}' 
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [myuser['email']]
        send_mail(subject, message, email_from, recipient_list)
       
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": auth_token[1]
        })


@api_view(['GET'])
def verify(request, token):
    print(token)
        # profile_obj = find_user_given_token(token)
    # user = Token.objects.get(key = token).user
    profile_obj = AuthToken.objects.filter(digest = token).first()
    print(profile_obj.user)
    if profile_obj:
        user = User.objects.get(id = profile_obj.user.id)
        user.is_active = True
        user.save()
        return Response("Your account has been verified. You can login now.")
    else:
        return Response("Please verify your account properly.")
    # return Response(token)




class LoginAPI(generics.GenericAPIView):

    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        # reset login tires
        login_tracker = LoginTracker.objects.get_or_create(username=user.username)[0]
        login_tracker.tries = 0
        login_tracker.save()
        # user_name = User.objects.filter(username = user.username)
        # print(user_name)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })
   

@api_view(['GET'])
def menuList(request, restaurant_slug=None):
    menus = Menu.objects.all()
    serializer =  MenuSerializer(menus, many= True)
    return Response(serializer.data)

@api_view(['GET'])
def menu(request, pk):
    menus = Menu.objects.filter(restaurant = pk)
    restaurant = Restaurant.objects.get(id = pk)

    serializer = MenuSerializer(menus, many= True)
    data = {
        'menu' : serializer.data,
        'restaurant': RestaurantSerializer(restaurant, many= False).data

    }
    return Response(data)



@api_view(['POST'])
def menuCreate(request):
  
    res = Restaurant.objects.filter(id=request.data['restaurant'])
    print(res)
    if res.exists():
        menu = Menu.objects.create(restaurant=res[0],dishname=request.data['dishname'],price=request.data['price'],image = request.data['image'])
        # serializer = MenuSerializer(data = menu, many=False)
        # if serializer.is_valid():
        #     serializer.save()
        # print(serializer)
        data={
        "message":"Added Successfully",
        # "data" :serializer.data
        "data": MenuSerializer(menu, many=False).data
        }
        print(data)
    else:
        data={
            "message":"Restaurant doesnot exist"
        }
    return Response(data)



@api_view(['POST'])
def menuUpdate(request,pk):
    menu = Menu.objects.get(id = pk)
    serializer = MenuSerializers(instance=menu, data = request.data)
    print(serializer)
    print(menu)
    
    if serializer.is_valid():
        serializer.save()
        data={
            "message":"Updated Successfully",
            "data": serializer.data,
        }
        print(data)
    else:
        data={
            "message":serializer.error_messages
        }
        return Response(data,status=500)

    return Response(data)



@api_view(['POST'])
def contactCreate(request):
    serializer = ContactSerializer(data = request.data)

    if serializer.is_valid():
        serializer.save()

    
    data={
        "message":"Message successfully sent",
        "data": serializer.data,
    }
    return Response(data)



@api_view(['DELETE'])
def menuDelete(request,pk):
    menu = Menu.objects.get(id = pk)
    menu.delete()

    return Response('Item successfully Deleted')


@api_view(['GET'])
def profile(request, pk):
    # profile = UserProfile.objects.filter(user = pk)
    # user = User.objects.get(id = pk)
    # serializer = ProfileSerializer(profile, many=False)
    profile = UserProfile.objects.filter(user = pk)
    user = User.objects.get(id = pk)
    print(profile)

    serializer = ProfileSerializer(profile, many= True)
    data = {
        'user' : serializer.data,
        'userlist': UserSerializer(user, many= False).data

    }
    return Response(data)




@api_view(['POST'])
def placeOrder(request):
    user = User.objects.filter(id=request.data['user'])
   
    if user.exists():
        tracking_no = str(random.randint(111111,999999))
        # print(request.data['phone'])
        # payment = request.POST.get()
        data_items = request.data['items']
        dict_obj = json.loads(data_items)
        print(dict_obj)
        total = 0.0
        for i in dict_obj:
            total += i['item']['price'] * i['qty']
        print(total)
        order = Order.objects.create(user=user[0],phone=request.data['phone'],address=request.data['address'],city=request.data['city'],state = request.data['state'], payment_way= request.data['payment_way'], tracking_no = tracking_no,items= request.data['items'], total_price = total)
        ord = Order.objects.all()
        # print(ord)
        data={
        "message":"Order Placed Successfully",
        # "data" :serializer.data
        "data": OrderSerializer(order, many = False).data
        }
        
        # print(dict_obj)
        # qty = list(map(itemgetter('qty'), dict_obj))
        # price = list(map(itemgetter('item.price'), dict_obj))
        
        # print(qty)
               
        return Response(data)
    else:
        data={
            "message":"Restaurant doesnot exist"
        }
        return Response(data,status=500)
    

@api_view(['POST'])
def profileCreate(request):
    user = User.objects.filter(id=request.data['user'])
    print(user)
    if user.exists():
        profile = UserProfile.objects.create(user=user[0],image = request.data['image'])
        print(profile)
        # serializer = MenuSerializer(data = menu, many=False)
        # if serializer.is_valid():
        #     serializer.save()
        # print(serializer)
        data={
        "message":"Profile Photo Added Successfully",
        # "data" :serializer.data
        "data": ProfileSerializer(profile, many=False).data
      }
    else:
        data={
            "message":"User doesnot exist"
        }
    return Response(data)    

@api_view(['POST'])
def profileUpdate(request,pk):
    userDetails = User.objects.get(id = pk)
    serializer = UserProfileSerializer(instance=userDetails, data = request.data)
    print(serializer)
    if serializer.is_valid():
        serializer.save()
        data={
            "message":"Updated Successfully",
            "data": serializer.data,
        }
        print(data)
    else:
        data={
            "message":serializer.error_messages
        }
        return Response(data,status=500)
        
    return Response(data)

@api_view(['GET'])
def reviewDetail(request, pk):
    review = Reviews.objects.filter(restaurant = pk)
    restaurant = Restaurant.objects.get(id = pk)
    # users = User.objects.filter(id=request.user)
    # print(request.data['user'])
    # users = request.data['user']
    # print(users)
    # user = User.objects.get(id = users)
    # print(users)

    serializer = ReviewSerializer(review, many= True)
    data = {
        'review' : serializer.data,
        'restaurant': RestaurantSerializer(restaurant, many= False).data,
        'user': UserDataSerializer(request.user, many=False).data

    }
    return Response(data)


@api_view(['POST'])
def postReview(request):
  
    res = Restaurant.objects.filter(id=request.data['restaurant'])
    user = User.objects.filter(id = request.data['user'])
    print(res)
    if res.exists() & user.exists():
        review = Reviews.objects.create(restaurant=res[0],user=user[0],reviews =request.data['reviews'])
     
        data={
            "message":"Added Successfully",
            "data": ReviewSerializer(review, many=False).data
        }
    else:
        data={
            "message":"Restaurant or user doesnot exist"
        }
    return Response(data)



@api_view(['DELETE'])
def reviewDelete(request,pk):
    review = Reviews.objects.get(id = pk)
    review.delete()

    return Response('Review successfully Deleted')


@api_view(['GET'])
def orderList(request, restaurant_slug=None):
   
    order = Order.objects.all()
 
    serializer =  OrderSerializer(order, many= True)
    return Response(serializer.data)


@api_view(['GET'])
def orderDetail(request, pk):
    order = Order.objects.filter(user = pk)
    user = User.objects.filter(request.data['user'])

    serializer = OrderSerializer(order, many= True)
    data = {
        'order' : serializer.data,
        'user': UserSerializer(user, many= False).data

    }
    return Response(data)

@api_view(['GET'])
def order(request, pk):
    order = Order.objects.get(id = pk)

    serializer = OrderSerializer(order, many= False)
    # data = {
    #     'data' : serializer.data,

    # }
    return Response(serializer.data)