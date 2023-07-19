from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
STATE_CHOICE = (
    ("Andaman and Nicobar Islands","Andaman and Nicobar Islands"),
    ("Andhra Pradesh","Andhra Pradesh"),
    ("Arunachal Pradesh","Arunachal Pradesh"),
    ("Assam","Assam"),
    ("Bihar","Bihar"),
    ("Chhattisgarh","Chhattisgarh"),
    ("Chandigarh","Chandigarh"),
    ("Dadra and Nagar Haveli and Daman & Diu","Dadra and Nagar Haveli and Daman & Diu"),
    ("Goa","Goa"),
    ("Gujarat","Gujarat"),
    ("Haryana","Haryana"),
    ("Himachal Pradesh","Himachal Pradesh"),
    ("Jammu & Kashmir","Jammu & Kashmir"),
    ("Jharkhand","Jharkhand"),
    ("Karnataka","Karnataka"),
    ("Kerala","Kerala"),
    ("Ladakh","Ladakh"),
    ("Lakshadweep","Lakshadweep"),
    ("Madhya Pradesh","Madhya Pradesh"),
    ("Maharashtra","Maharashtra"),
    ("Manipur","Manipur"),
    ("Meghalaya","Meghalaya"),
    ("Mizoram","Mizoram"),
    ("Nagaland","Nagaland"),
    ("Odisha","Odisha"),
    ("Puducherry","Puducherry"),
    ("Punjab","Punjab"),
    ("Rajasthan","Rajasthan"),
    ("Sikkim","Sikkim"),
    ("Tamil Nadu","Tamil Nadu"),
    ("Telangana","Telangana"),
    ("Tripura","Tripura"),
    ("Uttarakhand","Uttarakhand"),
    ("Uttar Pradesh","Uttar Pradesh"),
    ("West Bengal","West Bengal")
)

class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    locality = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICE, max_length=100)
   



    def __str__(self):
        return str(self.id)
    
CATEGORY_CHOICES = (
    ("M","Mobile"),
    ("L","Laptop"),
    ("TW","Top Wear"),
    ("BW","Bottom Wear"),   
)

class Product(models.Model):
    title = models.CharField(max_length=200)
    selling_price = models.FloatField()
    discount_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES ,max_length=25)
    product_image = models.ImageField(upload_to = "productimages")
    rating = models.DecimalField(decimal_places=1,max_digits=4)


    def __str__(self):
        return str(self.id)

class Cart(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    product = models.ForeignKey(Product, models.CASCADE)
    quantity =models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    @property
    def items_cost(self):
        return self.quantity * self.product.discount_price

    

STATUS_CHOICES = (
    ("Accepted","Accepted"),
    ("Packed","Packed"),
    ("On The Way","On The Way"),
    ("Delivered","Delivered"),
    ("Cancel","Your Order Cancel")
)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User,models.CASCADE)
    customer = models.ForeignKey(Customer, models.CASCADE)
    product =models.ForeignKey(Product,models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES,default="Pending")


    @property
    def amount(self):
        return self.quantity * self.product.discount_price



