from django.shortcuts import render,redirect,HttpResponse
from .models import *
from django.contrib import messages

# Create your views here.
from django.views.generic import View
from django.db.models import Q
from django.db.models import Sum,Count
import uuid
from django.contrib.auth import authenticate,login,logout

import razorpay

# paypal integration
from django.urls import reverse
from django.shortcuts import render
from paypal.standard.forms import PayPalPaymentsForm

addr=""
import json
def dashboard(request):
    try:
        data=product.objects.all()[:8]
        cart_count=0
        if request.user.is_authenticated:
            cart_count=cart.objects.filter(Q(user=request.user) & Q(buy=False)).count()
            a=address.objects.filter(user=request.user)
            if a.exists():
                global addr
                addr=True
            else:
                addr=False
        if "recent" not in request.session:
           request.session['recent'] = []
        recent=product.objects.filter(product_id__in=request.session['recent'])
        return render(request,'cart/dashboard.html',{'data':data,'addr':addr,'cart_count':cart_count,'recent':recent})
    except Exception as e:
        messages.info(request,e)
        return redirect('login')
def search(request):
    try:
        search_str=request.GET['search']
        data=product.objects.filter(Q(product_name__icontains=search_str) | Q(product_sub_cat__icontains=search_str) )
        cart_count=0
        if request.user.is_authenticated:
            cart_count=cart.objects.filter(Q(user=request.user) & Q(buy=False)).count()
            a=address.objects.filter(user=request.user)
            if a.exists():
                global addr
                addr=True
            else:
                addr=False
        return render(request,'cart/search.html',{'data':data,'addr':addr,'cart_count':cart_count})
    except Exception as e:
        messages.info(request,e)
    return redirect('dashboard')

class add_address(View):
    def get(self,request):
        if request.user.is_authenticated:
            adr=address.objects.filter(user=request.user,hide=False)
            restore=address.objects.filter(user=request.user,hide=True)
            cart_count=cart.objects.filter(Q(user=request.user) & Q(buy=False)).count()
            return render(request,"cart/add_address.html",{'cart_count':cart_count,'adr':adr,'restore':restore})
        else:
            return render(request,'account/login.html')
    def post(self,request):
        if request.method == 'POST':
            fname=request.POST.get('fname')
            lname=request.POST.get('lname')
            phone=request.POST.get('phone')
            alphone=request.POST.get('alphone')
            ad1=request.POST.get('ad1')
            ad2=request.POST.get('ad2')
            city=request.POST.get('city')
            state=request.POST.get('state')
            zip=request.POST.get('zip')
            add=address.objects.create(user=request.user,first_name=fname,last_name=lname,phone_number=phone,Alt_phone_number=alphone,line_1=ad1,line_2=ad2,city=city,state=state,pin_code=zip,hide=False)
            add.save()
            messages.info(request,"address Added Successfully")
            return redirect('add_address')

def set_default(request,id):
    try:
        if request.user.is_authenticated:
            r_default=address.objects.filter(Q(is_default=True) & Q(user=request.user))
            for i in r_default:
                i.is_default=False
                i.save()
            add=address.objects.get(add_id=id)
            add.is_default=True
            add.save()
            messages.info(request,"address set Successfully")
        else:
            return render(request,'account/login.html')
    except Exception as e:
        messages.info(request,e)
        return redirect('add_address')
    return redirect('add_address')
def restore(request,id):
    try:
        r_default=address.objects.get(add_id=id)
        r_default.hide=False
        r_default.is_default=True
        r_default.save()
    except Exception as e:
        messages.info(request,e)
        return redirect('add_address')
    return redirect('add_address')
def hide_address(request,id):
    try:
        r_default=address.objects.get(add_id=id)
        r_details=cart.objects.filter(address=r_default)
        print(r_details)
        if r_details.exists():
            r_default.hide=True
            r_default.is_default=False
            r_default.save()
        else:
            r_default.delete()
    except Exception as e:
        messages.info(request,e)
        return redirect('add_address')
    return redirect('add_address')
    

def add_to_cart(request,id):
    try:
        cart_data=cart.objects.filter(product_id=id ,user=request.user,buy=False)
        cart_count=[x.product_qty for x in cart_data]
        product_data=product.objects.get(product_id=id)
        product_price=product_data.product_disc_price
                
        if cart_data.exists():
            if cart_count[0] <5:
                total=(cart_count[0]*product_price)+product_price
                for i in cart_data:
                    i.product_qty=cart_count[0]+1
                    i.total_amount=total
                    i.save()
                messages.info(request,"Cart Updated Successfully")
            else:
                messages.info(request,"Cart limit is five only")
        else:
            add=cart.objects.create(user=request.user,product_id=product.objects.get(product_id=id),product_qty=1,total_amount=product_price)
            messages.info(request,"product added to cart Successfully")

        # recently viewed section
        # del request.session['recent']
        if "recent" not in request.session:
           request.session['recent'] = []
        if str(id) in request.session['recent']:
            request.session['recent'].remove(str(id))
            if len(request.session['recent']) >2:
                request.session['recent'].pop(0)
            request.session['recent']+=[id]
        else:
            if len(request.session['recent']) >2:
                request.session['recent'].pop(0)
            request.session['recent']+=[id]
        recent_data=request.session['recent']
        return redirect('dashboard')
    except Exception as e:
        messages.info(request,e)
        return redirect('dashboard')
def minus(request,id):
    cart_data=cart.objects.get(product_id=id ,user=request.user,buy=False)
    product_data=product.objects.get(product_id=id)
    product_price=product_data.product_disc_price
    if cart_data.product_qty >1:
        cart_count=cart_data.product_qty-1
        cart_price=cart_data.total_amount-product_price
        cart_data.product_qty=cart_count
        cart_data.total_amount=cart_price
        cart_data.save()
    else:
        cart_data.delete()
    return redirect('cart_data')
def plus(request,id):
    cart_data=cart.objects.get(product_id=id ,user=request.user,buy=False)
    product_data=product.objects.get(product_id=id)
    product_price=product_data.product_disc_price
    if cart_data.product_qty <5:
        cart_count=cart_data.product_qty+1
        cart_price=cart_data.total_amount+product_price
        cart_data.product_qty=cart_count
        cart_data.total_amount=cart_price
        cart_data.save()
    return redirect('cart_data')
def cart_data(request):
    try: 
        if request.user.is_authenticated:
            data=cart.objects.select_related('product_id').filter(Q(user=request.user) & Q(buy=False))
            cart_count=data.count()
            total=data.aggregate(Sum('total_amount'))
            context={
                'total':total,
                'data':data,
                'cart_count':cart_count,
            }
            return render(request,'cart/cart.html',context)
        else:
            return redirect('login')
    except Exception as e:
        messages.info(request,e)
        return render(request,'cart/dashboard.html')

def delete_cart_item(request,id):
    try:
        if request.user.is_authenticated:
            get_product=cart.objects.get(id=id).delete()
            messages.info(request,"deleted successfully")
            return redirect("cart_data")
        else:
            return redirect('login')
    except Exception as e:
        messages.info(request,e)
    return redirect("cart_data")

def clear_cart(request):
    try:
        if request.user.is_authenticated:
            cart.objects.filter(user=request.user,buy=False).delete()
            messages.info(request,"cart deleted successfully")
            return redirect("cart_data")
        else:
                return redirect('login')
    except Exception as e:
        messages.info(request,e)
        return redirect("cart_data")


def buy_now(request,id):
    try:
        if request.user.is_authenticated:
            cart_data=cart.objects.filter(product_id=id ,user=request.user,buy=False)
            cart_count=[x.product_qty for x in cart_data]
            product_data=product.objects.get(product_id=id)
            product_price=product_data.product_disc_price
                    
            if cart_data.exists():
                if cart_count[0] <5:
                    total=(cart_count[0]*product_price)+product_price
                    for i in cart_data:
                        i.product_qty=cart_count[0]+1
                        i.total_amount=total
                        i.save()
                    messages.info(request,"Cart Updated Successfully")
                else:
                    messages.info(request,"Cart limit is five only")
                return redirect('cart_data') 
            else:
                add=cart.objects.create(user=request.user,product_id=product.objects.get(product_id=id),product_qty=1,total_amount=product_price)
                messages.info(request,"product added to cart Successfully")
                return redirect('buy_page' ,id )
        else:
            return redirect('login')
    except Exception as e:
        messages.info(request,e)
        return redirect('dashboard')

def place_order(request,id):
    try:
        if request.user.is_authenticated:
            cart_update=cart.objects.get(product_id=id,user=request.user,buy=False)
            cart_qty=cart_update.product_qty
            cart_update.buy=True
            cart_update.address=address.objects.get(user=request.user,is_default=True)
            cart_update.payment_type='cod'
            o_id=uuid.uuid4()
            cart_update.order_id=o_id
            cart_update.save()

            product_data=product.objects.get(product_id=id)
            p_qty=product_data.product_qty
            product_data.product_qty=p_qty-cart_qty
            product_data.save()
            order_confirm=order.objects.create(user=request.user,cart=cart_update,total_amount=cart_update.total_amount,order_id=o_id,payment_status='Not Paid')
            order_confirm.save()
            delivery_status.objects.create(order_id=order_confirm,status='Processing')
            messages.info(request,'order placed Successfully')
            return render(request,'cart/order_success.html') 
        else:
                return redirect('login')
    except Exception as e:
        messages.info(request,e)
        return redirect('cart_data') 

def test(request):
    return render(request,'cart/order_success.html')

from django.conf import settings
def buy_page(request,id):
    if request.user.is_authenticated:
        product_data=cart.objects.get(product_id=id,user=request.user,buy=False)
        adr=address.objects.filter(user=request.user,is_default=True)
        cart_count=cart.objects.filter(Q(user=request.user) & Q(buy=False)).count()
        # razorpay Payment

        total=product_data.total_amount *100
        client= razorpay.Client(auth=(settings.KEY,settings.SECRET))
        payment=client.order.create({'amount':total,'currency':'INR'})
        usd=product_data.total_amount/83.36
        # paypal payment
        order_id=uuid.uuid4()
        paypal_dict = {
                "business": "sb-ktu8d20578368@business.example.com",
                "amount": usd,
                "item_name": product_data.product_id.product_name,
                "invoice":order_id,
                'currency_code': 'USD',
                "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
                "return": request.build_absolute_uri(reverse('success_p',kwargs={'product_id':product_data.product_id,'order_id':order_id})),
                "cancel_return": request.build_absolute_uri(reverse('failed_paypal')),
            }
        form = PayPalPaymentsForm(initial=paypal_dict)
        return render(request,"cart/buy_page.html",{'cart_count':cart_count,'adr':adr,'product_data':product_data,"form": form,'payment':payment})
    else:
        return redirect('login')
def success_paypal(request,product_id,order_id):
    payment_id=request.GET['PayerID']
    try:
        if request.user.is_authenticated:
            cart_update=cart.objects.get(product_id=product_id,user=request.user,buy=False)
            cart_qty=cart_update.product_qty
            cart_update.address=address.objects.get(user=request.user,is_default=True)
            cart_update.buy=True
            cart_update.payment_id=payment_id
            cart_update.payment_type='online'
            cart_update.save()

            product_data=product.objects.get(product_id=product_id)
            p_qty=product_data.product_qty
            product_data.product_qty=p_qty-cart_qty
            product_data.save()

            order_confirm=order.objects.create(user=request.user,cart=cart_update,total_amount=cart_update.total_amount,payment_id=payment_id,order_id=order_id,payment_status='PAID BY PAYPAL')
            order_confirm.save()
            delivery_status.objects.create(order_id=order_confirm,status='Processing')
            cart_count=cart.objects.filter(user=request.user,buy=False).count()
            messages.info(request,"Payment successful ,Order Placed Successfully")
            return render(request,'cart/order_success.html',{'cart_count':cart_count})
        else:
            return redirect('login')
    except Exception as e:
        print(e)
    return redirect('cart_data')

def failed_paypal(request):
    cart_count=cart.objects.filter(user=request.user,buy=False).count()
    return render(request,'cart/order_failed.html',{'cart_count':cart_count})
def success(request):
    p_id=request.GET['product_id']
    o_id=request.GET['order_id']
    payment_id=request.GET['payment_id']
    try:
        cart_update=cart.objects.get(product_id=p_id,user=request.user,buy=False)
        cart_qty=cart_update.product_qty
        cart_update.address=address.objects.get(user=request.user,is_default=True)
        cart_update.buy=True
        cart_update.payment_id=payment_id
        cart_update.payment_type='online'
        cart_update.save()

        product_data=product.objects.get(product_id=p_id)
        p_qty=product_data.product_qty
        product_data.product_qty=p_qty-cart_qty
        product_data.save()

        order_confirm=order.objects.create(user=request.user,cart=cart_update,total_amount=cart_update.total_amount,order_id=o_id,payment_id=p_id,payment_status='PAID BY RAZORPAY')
        order_confirm.save()
        delivery_status.objects.create(order_id=order_confirm,status='Processing')
        cart_count=cart.objects.filter(user=request.user,buy=False).count()
        messages.info(request,"Payment successful ,Order Placed Successfully")
        return render(request,'cart/order_success.html',{'cart_count':cart_count})
        
    except Exception as e:
        print(e)
    return redirect('cart_data')
def failed(request):
    order_id=request.GET['order_id'] 
    product_id=request.GET['product_id'] 
    cart_count=cart.objects.filter(user=request.user,buy=False).count()
    return render(request,'cart/order_failed.html',{'cart_count':cart_count})

def my_orders(request):
    try:
        if request.user.is_authenticated:
            cart_count=cart.objects.filter(Q(user=request.user) & Q(buy=False)).count()
            orders=order.objects.filter(user=request.user).order_by('-date_of_payment')
            d_status=delivery_status.objects.all()
            return render(request,"cart/my_orders.html",{'orders':orders,'cart_count':cart_count,'d_status':d_status})
        else:
            return redirect('login')
    except Exception as e:
        messages.info(request,e)



def updates(request):
    if request.method =="POST":
        email=request.POST['newsletter']
        indb , created=newsletter.objects.get_or_create(email=email)
        if created:
            messages.info(request,"Registered Successfully")
        else:
            messages.info(request,"Already Registered")

    return redirect(dashboard)