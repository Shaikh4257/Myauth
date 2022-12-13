from django.shortcuts import render, redirect
from accounts.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,EmptyPage

# Create your views here.
def start(request):
    return render(request, 'home.html')


def register(request):
    error=""
    if request.method == 'POST':
        email = request.POST.get('email')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        dateofbirth=request.POST.get('dob')
        gender=request.POST.get('gender')
        type=request.POST.get('type')
        phonenumber=request.POST.get('phone')
        password = request.POST.get('newpassword')
        try:
            user=User.objects.create_user(email,firstname,lastname,dateofbirth,gender,type,phonenumber,password)
            error="no"
        except:
            error="yes"
    return render(request,'signup.html',{"error":error})


def signin(request):
    error=""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pass1')
        user = authenticate(email = username, password = password)
        if user is not None :
            print("user")
            login(request, user)
            error="no"
        else:
            error="yes"
    return render(request, 'signin.html',{"error":error})




@login_required()
def dashboard(request):
    user=User.objects.all()
    p=Paginator(user,5)
    page_num= request.GET.get('page',1)
    try:
        page=p.page(page_num)
    except EmptyPage:
        page=p.page(1)
    return render(request, 'dashboard.html',{"user":page})


def searchmatch(query,user):
    if query in user.first_name.lower() or query in user.last_name.lower() or query in user.email.lower() or query in user.phonenumber.lower() or query in user.type.lower() :
       # print(item.product_name)
        return True
    else:
        return False

def search(request):
    query=request.GET.get('search')
    alluser=User.objects.all()
    result=[ user for user in alluser if searchmatch(query,user) ]
    return render(request, 'search.html',{"result":result})


@login_required()
def UpdateProfile(request):
    user=User.objects.get(id=request.user.id)
    error=""
    if request.method=="POST":
        email = request.POST.get('email')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        dateofbirth=request.POST.get('dob')
        gender=request.POST.get('gender')
        phonenumber=request.POST.get('phone')
        user.email=email
        user.first_name=firstname
        user.last_name=lastname
        user.date_of_birth=dateofbirth
        user.gender=gender
        user.phonenumber=phonenumber
        try:
            user.save()
            error="no"
        except:
            error="yes"
    return render(request,'updateprofile.html',{"user":user})


def changePassword(request):
    error = ""
    user = request.user
    if request.method == "POST":
        o = request.POST['oldpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if user.check_password(o):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error = 'not'
        except:
            error = "yes"
    return render(request, 'changepassword.html', locals())

def Logout(request):
    logout(request)
    return redirect('home')