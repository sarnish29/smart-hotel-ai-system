from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    category_title = models.CharField(max_length=200)
    category_gif = models.CharField(max_length=200)
    category_description = models.TextField(max_length=400, default= 'Enjoy the meal!!') #make this the wysiwyg text field

    def __str__(self):
        #overriding the string method to get a good representation of it in string format
        return f"{self.category_title}"

class PakistaniCuisine(models.Model):
    dish_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        #overriding the string method to get a good representation of it in string format
        return f"{self.dish_name}"

class MexicanCuisine(models.Model):
    dish_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        #overriding the string method to get a good representation of it in string format
        return f"{self.dish_name}"

class ItalianCuisine(models.Model):
    dish_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        #overriding the string method to get a good representation of it in string format
        return f"{self.dish_name}"
class FrenchCuisine(models.Model):
    dish_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        #overriding the string method to get a good representation of it in string format
        return f"{self.dish_name}"
class TurkishCuisine(models.Model):
    dish_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        #overriding the string method to get a good representation of it in string format
        return f"{self.dish_name}"

# class UserOrder(models.Model):
#     username = models.ForeignKey(User, related_name='order', on_delete=models.CASCADE) #who placed the order
#     order = models.TextField(default=None) #this will be a string representation of the cart from localStorage
#     price = models.DecimalField(max_digits=6, decimal_places=2) #how much was the order
#     time_of_order  = models.DateTimeField(default=datetime.now, blank=True)
#     delivered = models.BooleanField()
#
#     def __str__(self):
#         #overriding the string method to get a good representation of it in string format
#         return f"Order placed by  : {self.username} on {self.time_of_order.date()} at {self.time_of_order.time().strftime('%H:%M:%S')}"
#
# class SavedCarts(models.Model):
#     username = models.ForeignKey(User, related_name='cart', on_delete=models.CASCADE)
#     cart = models.TextField() #this will be a string representation of the cart from localStorage
#
#     def __str__(self):
#         #overriding the string method to get a good representation of it in string format
#         return f"Saved cart for {self.username}"

class UserOrder(models.Model):
    username = models.CharField(max_length=200) #who placed the order
    order = models.TextField() #this will be a string representation of the cart from localStorage
    price = models.DecimalField(max_digits=6, decimal_places=2) #how much was the order
    time_of_order  = models.DateTimeField(default=datetime.now, blank=True)
    delivered = models.BooleanField()

    def __str__(self):
        #overriding the string method to get a good representation of it in string format
        return f"Order placed by  : {self.username} on {self.time_of_order.date()} at {self.time_of_order.time().strftime('%H:%M:%S')}"

class SavedCarts(models.Model):
    username = models.CharField(max_length=200, primary_key=True)
    cart = models.TextField() #this will be a string representation of the cart from localStorage

    def __str__(self):
        #overriding the string method to get a good representation of it in string format
        return f"Saved cart for {self.username}"