# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils import timezone
# Create your models here.

class Restaurant(models.Model):
    Name = models.CharField(max_length=200)
    place = models.CharField(max_length=150)
    Types = models.CharField(max_length=250)
    Img = models.ImageField(upload_to='images/', height_field=None, width_field=None,blank = True)
    featured = models.BooleanField(default=False, help_text="0=default, 1=hidden")
    special = models.BooleanField(default=False,help_text="0=default, 1=hidden")
    # parent = models.ForeignKey('self', null = True, blank=True,related_name='children',on_delete=models.PROTECT)
   
    def __str__(self):
        return self.Name

class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='details', on_delete= models.CASCADE)
    dishname = models.CharField(max_length=200,null=False,blank=False)
    price = models.PositiveIntegerField(null=False, blank=False)
    image = models.ImageField(upload_to='images/', height_field=None, width_field=None,blank = True)

class Contact(models.Model):
    first_name = models.CharField(max_length=150,null=False,blank=False)
    last_name = models.CharField(max_length=150,null=False,blank=False)
    email = models.CharField(max_length=200,null=False,blank=False)
    message = models.CharField(max_length=500,null=False,blank=False)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', height_field=None, width_field=None,blank = True)

    # def __str__(self):
    #     return f'{self.user.username} UserProfile'

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length= 150, null=False)
    city = models.CharField(max_length=150, null = False)
    state = models.CharField(max_length=150, null=False)
    orderstatus = (
        ('Pending','Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Completed','Completed')
    )
    status = models.CharField(max_length=150, choices=orderstatus, default='Pending')
    message = models.TextField(null = True, blank=True)
    payment = (
        ('Cash on Delivery','Cash on Delivery'),
        ('Khalti','Khalti')
    )
    payment_way = models.CharField(max_length=150, choices=payment, default='Cash on Delivery')
    tracking_no = models.CharField(max_length=150, null=True)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now=True)
    items = models.TextField(null=True)
    total_price = models.IntegerField(null=True)

    def __str__(self):
        return '{} - {}'.format(self.id, self.tracking_no)

# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete= models.CASCADE)
#     menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
#     price = models.FloatField(null = False)
#     quantity = models.IntegerField(null=False)

#     def __str__(self):
#         return '{} {}'.format(self.order.id, self.order.tracking_no) 

class Reviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    reviews = models.TextField(max_length=350, null=True)

class LoginTracker(models.Model):
    username = models.EmailField(null=True,blank=True)
    tries = models.IntegerField(default=0)

    modified_on = models.DateTimeField(auto_now=True)

    def valid_login(self):
        if self.tries <=5 or self.modified_on+timedelta(minutes=3)<timezone.now():
            return True, True
        time_left = self.modified_on+timedelta(minutes=3)-timezone.now()
        minutes = time_left.seconds // 60
        seconds = time_left.seconds % 60

        formatted_time = f"{minutes:02d}:{seconds:02d}"
        return False, formatted_time
    
    def add_try(self):
        self.tries+=1
        self.save()


