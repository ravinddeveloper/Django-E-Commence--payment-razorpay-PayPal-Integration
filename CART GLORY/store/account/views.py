from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
# Create your views here.
def handle_login(request):
    if request.method=="POST":
        uname=request.POST.get("username")
        pass1=request.POST.get("pass1")
        user=authenticate(request,username=uname,password=pass1)
        if user is not None:
            login(request,user)
            messages.info(request,"Login Successful")
            return redirect('dashboard')
        
    return render(request,"account/login.html")

def handle_register(request):
    try:
        if request.method=="POST":
            uname=request.POST.get("username")
            fname=request.POST.get("fname")
            lname=request.POST.get("lname")
            email=request.POST.get("email")
            pass1=request.POST.get("pass1")
            pass2=request.POST.get("pass2")
            user=User.objects.filter(username=uname)
            mail=User.objects.filter(email=email)
        
            if user.exists():
                messages.info(request,"Username taken")
                return render(request,"account/register.html")
            elif mail.exists():
                messages.info(request,"Email already Registered")
                return render(request,"account/register.html")
            elif pass1 !=pass2:
                messages.info(request,"password is not match")
                return render(request,"account/register.html")
            else:
                user=User.objects.create(username=uname,first_name=fname,last_name=lname,email=email)
                user.set_password(pass1)
                user.save()
                messages.info(request,"User Registered Successfully")
                return render(request,"account/register.html")
        return render(request,"account/register.html")
    except Exception as e:
        messages.info(request,e)
        return render(request,"account/register.html")

def handle_logout(request):
    logout(request)
    return render(request,"account/register.html")


def profile(request):
    try:
        data=User.objects.get(username=request.user)
        # data1=Profile.
    except Exception as e:
        messages.info(request,e)
        