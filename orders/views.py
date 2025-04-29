from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import SavedCarts
from .models import *
from django.contrib.auth import logout, authenticate, login
import json

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        #we are passing in the data from the category model
        return render(request, "orders/home.html", {"categories":Category.objects.all})
    else:
        return redirect("/user/login")

# def login_request(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request=request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 login(request, user)

#                 return redirect('/')

#     form = AuthenticationForm()
#     return render(request = request,
#                     template_name = "orders/login.html",
#                     context={"form":form})

def logout_request(request):
    logout(request)
    return redirect("orders:login")

# def register(request):
#     if request.method == "POST":
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             username = form.cleaned_data.get('username')
#             login(request, user)
#             return redirect("orders:index")

#         return render(request = request,
#                           template_name = "orders/register.html",
#                           context={"form":form})

#     return render(request = request,
#                   template_name = "orders/register.html",
#                   context={"form":UserCreationForm})

# def pizza(request):
#     if request.user.is_authenticated:
#         return render(request, "orders/pizza.html", context = {"regular_pizza":RegularPizza.objects.all, "sicillian_pizza":SicilianPizza.objects.all , "toppings":Toppings.objects.all, "number_of_toppings":[1,2,3]})
#     else:
#         return redirect("/user/login")

def pakistani_cuisine(request):
    if request.user.is_authenticated:
        return render(request, "orders/pakistani.html", context = {"dishes":PakistaniCuisine.objects.all})
    else:
        return redirect("/user/login")

def mexican_cuisine(request):
    if request.user.is_authenticated:
        return render(request, "orders/mexican.html", context = {"dishes":MexicanCuisine.objects.all})
    else:
        return redirect("/user/login")

def french_cuisine(request):
    if request.user.is_authenticated:
        return render(request, "orders/french.html", context = {"dishes":FrenchCuisine.objects.all})
    else:
        return redirect("/user/login")

def italian_cuisine(request):
    if request.user.is_authenticated:
        return render(request, "orders/italian.html", context = {"dishes":ItalianCuisine.objects.all})
    else:
        return redirect("/user/login")

def turkish_cuisine(request):
    if request.user.is_authenticated:
        return render(request, "orders/turkish.html", context = {"dishes":TurkishCuisine.objects.all})
    else:
        return redirect("/user/login")


#
# def cart(request):
#     if request.user.is_authenticated:
#         return render(request, "orders/cart.html")
#     else:
#         return redirect("/user/login")
#
# def checkout(request):
#     if request.method == 'POST':
#         cart = json.loads(request.POST.get('cart'))
#         price = request.POST.get('price_of_cart')
#         username = request.user.id
#         response_data = {}
#         list_of_items = [item["item_description"] for item in cart]
#
#         order = UserOrder(username=username, order=list_of_items, price=float(price), delivered=False) #create the row entry
#         order.save() #save row entry in database
#
#         response_data['result'] = 'Order Recieved!'
#
#         return HttpResponse(
#             json.dumps(response_data),
#             content_type="application/json"
#         )
#     else:
#         return HttpResponse(
#             json.dumps({"nothing to see": "this isn't happening"}),
#             content_type="application/json"
#         )
#
# def view_orders(request):
#     if request.user.is_staff:
#         #make a request for all the orders in the database
#         rows = UserOrder.objects.all().order_by('-time_of_order')
#         #orders.append(row.order[1:-1].split(","))
#
#         return render(request, "orders/orders.html", context = {"rows":rows})
#     else:
#         rows = UserOrder.objects.all().filter(username = request.user.id).order_by('-time_of_order')
#         return render(request, "orders/orders.html", context = {"rows":rows})
#
# def mark_order_as_delivered(request):
#     if request.method == 'POST':
#         id = request.POST.get('id')
#         UserOrder.objects.filter(pk=id).update(delivered=True)
#         return HttpResponse(
#             json.dumps({"good":"boy"}),
#             content_type="application/json"
#         )
#     else:
#         return HttpResponse(
#             json.dumps({"nothing to see": "this isn't happening"}),
#             content_type="application/json"
#         )
#
# def save_cart(request):
#     if request.method == 'POST':
#         cart = request.POST.get('cart')
#         saved_cart = SavedCarts(username=request.user.id, cart=cart) #create the row entry
#         saved_cart.save() #save row entry in database
#         return HttpResponse(
#             json.dumps({"good":"boy"}),
#             content_type="application/json"
#         )
#     else:
#         return HttpResponse(
#             json.dumps({"nothing to see": "this isn't happening"}),
#             content_type="application/json"
#         )
#
# def retrieve_saved_cart(request):
#     saved_cart = SavedCarts.objects.get(username = request.user.id)
#     return HttpResponse(saved_cart.cart)
#
# def check_superuser(request):
#     print(f"User super??? {request.user.is_staff}")
#     return HttpResponse(request.user.is_staff)

def cart(request):
    if request.user.is_authenticated:
        return render(request, "orders/cart.html")
    else:
        return redirect("/user/login")

def checkout(request):
    if request.method == 'POST':
        cart = json.loads(request.POST.get('cart'))
        price = request.POST.get('price_of_cart')
        username = request.user.username
        response_data = {}
        list_of_items = [item["item_description"] for item in cart]

        order = UserOrder(username=username, order=list_of_items, price=float(price), delivered=False) #create the row entry
        order.save() #save row entry in database

        response_data['result'] = 'Order Recieved!'

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

def view_orders(request):
    if request.user.is_superuser:
        #make a request for all the orders in the database
        rows = UserOrder.objects.all().order_by('-time_of_order')
        #orders.append(row.order[1:-1].split(","))

        return render(request, "orders/orders.html", context = {"rows":rows})
    else:
        rows = UserOrder.objects.all().filter(username = request.user.username).order_by('-time_of_order')
        return render(request, "orders/orders.html", context = {"rows":rows})

def mark_order_as_delivered(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        UserOrder.objects.filter(pk=id).update(delivered=True)
        return HttpResponse(
            json.dumps({"good":"boy"}),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

def save_cart(request):
    if request.method == 'POST':
        cart = request.POST.get('cart')
        saved_cart = SavedCarts.objects.create(username=request.user.username, cart=cart) #create the row entry
        saved_cart.save() #save row entry in database
        return HttpResponse(
            json.dumps({"good":"boy"}),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

def retrieve_saved_cart(request):
    if request.user.is_authenticated:
        try:
            saved_cart = SavedCarts.objects.get(username=request.user.username)
            return render(request, 'orders/cart.html', {'cart': saved_cart})
        except SavedCarts.DoesNotExist:
            messages.info(request, "No saved cart found.")
            return redirect('orders:index')  
    else:
        messages.error(request, "Please log in to view your saved cart.")
        return redirect('login') 
    
def check_superuser(request):
    print(f"User super??? {request.user.is_superuser}")
    return HttpResponse(request.user.is_superuser)