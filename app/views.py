from django.shortcuts import render, redirect
from django.views import View
from .models import Product, Customer, Cart, OrderPlaced
from .forms import CustomerRegistration, CustomerProfile
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



class ProductView(View):
    def get(self, request):
        topwear = Product.objects.filter(category = "TW")
        bottomwear = Product.objects.filter(category = "BW")
        mobiles = Product.objects.filter(category = "M")
        return render(request, 'app/home.html',{"topwear":topwear,"bottomwear":bottomwear, "mobile":mobiles})
    

class ProductDetails(View):
    def get(self, request,id): 
        product = Product.objects.get(pk= id)
        item_already_in_cart = False
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(Q(product = product.id)& Q(user = request.user)).exists()
        return render(request, 'app/productdetail.html',{"product":product ,"item_in_cart":item_already_in_cart})
    
 
@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get("prod_id")
    product = Product.objects.get(id = product_id)
    print(product_id,product)
    Cart(user = user, product = product).save()
    return redirect("/cart")



# @login_required
# def add_to_cart(request):
#     user = request.user
#     product_id = request.GET.get("prod_id")
#     product = Product.objects.get(id = product_id)
#     saved_reports = Cart.objects.all()
#     match_id = []
#     for report in saved_reports:
#         match_id.append(report.product.pk)
#     print(report.product.pk,match_id,product)

#     if product not in match_id:
#         print("priya")
#         Cart(user = user, product = product).save()
#     else:
#         print("p")
#         messages.success(request, "This product already added in your cart.")
#     return redirect("/cart")


@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user = user)
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity*p.product.discount_price)
                amount +=tempamount
                totalamount = amount+shipping_amount
            return render(request, "app/addtocart.html",{"carts":cart,"totalamount":totalamount,"amount":amount,"shipping":shipping_amount})
        else:
            return render(request, "app/emptycart.html")



def plus_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product = prod_id) & Q(user= request.user))
        c.quantity +=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discount_price )
            amount+=tempamount
            totalamount = amount + shipping_amount
        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)





def minus_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product = prod_id) & Q(user= request.user))
        c.quantity-=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discount_price )
            amount+=tempamount
            totalamount = amount + shipping_amount
        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)



def remove_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product = prod_id) & Q(user= request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discount_price )
            amount+=tempamount
            totalamount = amount + shipping_amount
        data = {
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)



def buy_now(request):
    return render(request, 'app/buynow.html')

def profile(request):
    return render(request, 'app/profile.html')

@login_required
def address(request):
    address = Customer.objects.filter(user= request.user)
    return render(request, 'app/address.html',{"add":address,"active":"btn-primary"})


@login_required
def orders(request):
    orders = OrderPlaced.objects.filter(user = request.user)
    return render(request, 'app/orders.html',{"ord":orders})



def mobile(request,data = None):
    if data == None:
        mobiles = Product.objects.filter(category = "M")
    elif data == "Redmi" or data == "Samsung" or data == "infinix":
        mobiles = Product.objects.filter(category = "M").filter(brand = data)
    elif data == "below":
        mobiles = Product.objects.filter(category = "M").filter(discount_price__lt = 10000)
    elif data == "above":
        mobiles = Product.objects.filter(category = "M").filter(discount_price__gt = 10000)
    return render(request, 'app/mobile.html',{"mobiles":mobiles})


def laptop(request,data = None):
    if data == None:
        mobiles = Product.objects.filter(category = "L")
    elif data == "Asus" or data == "Hp" or data == "Dell" or data == 'Apple':
        laptops = Product.objects.filter(category = "L").filter(brand = data)
    elif data == "below":
        laptops = Product.objects.filter(category = "L").filter(discount_price__lt = 10000)
    elif data == "above":
        laptops = Product.objects.filter(category = "L").filter(discount_price__gt = 10000)
    return render(request, 'app/laptop.html',{"laptop":laptops})





def topwear(request,data = None):
    if data == None:
        topwear = Product.objects.filter(category = "TW")
    elif data == "below":
        topwear = Product.objects.filter(category = 'TW').filter(discount_price__lt = 500)
    elif data == "above":
        topwear = Product.objects.filter(category = "TW").filter(discount_price__gt = 500)
    return render(request, 'app/topwear.html',{"tops":topwear})




def bottomwear(request,data = None):
    if data == None:
        bottomwear = Product.objects.filter(category = "BW")
    elif data == "below":
        bottomwear = Product.objects.filter(category = 'BW').filter(discount_price__lt = 500)
    elif data == "above":
        bottomwear = Product.objects.filter(category = "BW").filter(discount_price__gt = 500)
    return render(request, 'app/bottomwear.html',{"bottoms":bottomwear})



class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistration()
        return render(request,'app/customerregistration.html',{"form":form})
    
    def post(self, request):
        form = CustomerRegistration(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Your account has been created successfully!")
            #return redirect('home')
        return render(request,'app/customerregistration.html',{"form":form})
            
    

@login_required
def checkout(request):
 user = request.user
 add = Customer.objects.filter(user = user)
 cart_items = Cart.objects.filter(user = user)
 amount= 0.0
 shipping_amount = 70.0
 totalamount = 0.0
 cart_product = [p for p in Cart.objects.all() if p.user == request.user]
 if cart_product:
    for p in cart_product:
        tempamount = (p.quantity * p.product.discount_price )
        amount+=tempamount
    totalamount = amount+shipping_amount
 return render(request, 'app/checkout.html',{"add":add,"totalamount":totalamount,"cart":cart_items})

@login_required
def paymentdone(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id = custid)
    cart = Cart.objects.filter(user =user)
    for c in cart:
        OrderPlaced(user = user, customer =customer,product = c.product, quantity =c.quantity).save()
        c.delete()
    return redirect("orders")



@method_decorator(login_required, name="dispatch")
class ProfileView(View):
    def get(self, request):
        form = CustomerProfile()
        return render(request, "app/profile.html",{"form":form,"active":"btn-primary"})
    
    def post(get,request):
        customer=CustomerProfile(request.POST)
        print("hello world")
        if customer.is_valid():
            user = request.user
            name = customer.cleaned_data["name"]
            locality = customer.cleaned_data['locality']
            city = customer.cleaned_data['city']
            state = customer.cleaned_data['state']
            zipcode = customer.cleaned_data['zipcode']

            reg = Customer(user = user, name = name, locality = locality, city =city, state= state , zipcode = zipcode)
            reg.save()    
            messages.success(request, "Congratulations !! Your Profile Updated Successfully.")
        return render(request,"app/profile.html",{"form":customer,"active":'btn-primary'})
            


