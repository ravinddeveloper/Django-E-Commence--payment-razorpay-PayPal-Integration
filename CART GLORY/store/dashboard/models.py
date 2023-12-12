from django.db import models
from django_extensions.db.fields import AutoSlugField
from django.contrib.auth.models import User
import uuid
# Create your models here.
class category(models.Model):
    category=models.CharField(max_length=50,default=None)

    def __str__(self):
        return self.category
class product(models.Model):
    product_id=models.AutoField(primary_key=True)
    product_name=models.CharField(max_length=50)
    slug=AutoSlugField(populate_from=('product_name',))
    product_cat=models.ForeignKey(category, on_delete=models.CASCADE,related_name='cat')
    product_sub_cat=models.CharField(max_length=50)
    product_desc=models.CharField(max_length=100)
    product_price=models.IntegerField()
    product_disc_price=models.IntegerField()
    product_img1=models.ImageField(upload_to="product_img")
    product_img2=models.ImageField(upload_to="product_img")
    product_qty=models.IntegerField()
    
    def __str__(self):
        return str(self.product_id)
    

class address(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    add_id=models.AutoField(primary_key=True)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    phone_number=models.IntegerField()
    Alt_phone_number=models.IntegerField()
    line_1=models.CharField(max_length=50)
    line_2=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    pin_code=models.IntegerField()
    hide=models.BooleanField(default=False)
    is_default=models.BooleanField(default=False)

class cart(models.Model):
    pay=(
        ('online','online'),
        ('cod','cod'),
    )
    user=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product_id=models.ForeignKey(product,null=True, blank=True ,on_delete=models.SET_NULL,related_name="cart")
    Added_date=models.DateTimeField(auto_now=True)
    product_qty=models.IntegerField()
    total_amount=models.IntegerField()
    address=models.ForeignKey(address, on_delete=models.SET_NULL, null=True)
    buy=models.BooleanField(default=False)
    payment_type=models.CharField(choices = pay ,default='cod',max_length=50) 
    order_id=models.CharField(max_length=100,null=True, blank=True)
    payment_id=models.CharField(max_length=100,null=True, blank=True)
    

    def __str__(self):
        return str(self.product_id)
    
class order(models.Model):
    user=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    cart=models.ForeignKey(cart, on_delete=models.SET_NULL, null=True,related_name="order")
    total_amount=models.IntegerField()
    order_id=models.CharField(max_length=100,null=True, blank=True)
    payment_id=models.CharField(max_length=100,null=True, blank=True)
    payment_status=models.CharField(max_length=100,null=True, blank=True)
    date_of_payment=models.DateTimeField(auto_now=True) 

class delivery_status(models.Model):
    ch=(
        ('Processing','Processing'),
        ('Shipped','Shipped'),
        ('arrived','arrived'),
        ('delivered','delivered'),
        ('OFD','OFD'),
        ('Rejected','Rejected'),
        ('Returned','Returned'),
        ('canceled','canceled'),
    )
    refund=(
        ('initiated','initiated'),
        ('completed','completed'),
        ('none','none'),
    )
    order_id=models.ForeignKey(order, on_delete=models.SET_NULL, null=True)
    refund_status=models.CharField(choices = refund ,default='none',max_length=50)
    status=models.CharField(choices = ch ,default='Processing',max_length=50) 

class newsletter(models.Model):
    email=models.EmailField()

    def __str__(self):
        return self.email



