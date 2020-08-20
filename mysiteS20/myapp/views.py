import sys
from django.shortcuts import render, redirect, reverse
# Import necessary classes
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, Http404

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from . import forms
from .forms import OrderForm, InterestForm, UserForm, UserProfileInfoForm
from .models import Topic, Course, Student, Order
from datetime import datetime

# Create your views here.

def courses(request):
    courlist = Course.objects.all().order_by('id')
    return render(request, 'myapp/courses.html', {'courlist': courlist})

def index(request):
    top_list = Topic.objects.all().order_by('id')[:10]

    #For Last Login
    if request.COOKIES.get('last_login'):
        login_time = request.COOKIES.get('last_login')
    else:
        login_time = 'Your last login was more than one hour ago'
    response = HttpResponse(render(request, 'myapp/index.html', {'top_list': top_list, 'login_time': login_time}))
    response.set_cookie('last_login', login_time, max_age=5)
    response.delete_cookie('last_login', login_time)

    #For Visit Counter
    about_visits = int(request.COOKIES.get('about_visits', '0'))
    response.set_cookie('about_visits', about_visits + 1)
    return response
    #  Are you passing any extra context variables to the template? If so, what are you passing?
    # Answer: Yes we are passing Topic list by their order id so that in index.html we can list all the topics

def about(request):

    #if request.session.test_cookie_worked():
    #    print("The Test Cookies worked")
    #    request.session.delete_test_cookie()

    #For Visit Counter
    if request.COOKIES.get('about_visits'):
        mynum = request.COOKIES.get('about_visits')
    else:
        mynum = 0
    response = render(request, 'myapp/about.html', {'mynum' : mynum})
    response.set_cookie('about_visits', mynum, expires=5)
    response.delete_cookie('about_visits', mynum)
    return response
    #return render(request, 'myapp/about.html')
    # Do you need to pass any extra context variables to the template?
    # Answer: No we dont need to pass any extra variable for this as this page is only for display


def detail(request, top_no):
    top_list = Topic.objects.filter(id=top_no)
    c_list = Course.objects.all()
    get_object_or_404(top_list, id=top_no)
    return render(request, 'myapp/detail.html', {'top_list': top_list, 'c_list': c_list})
    # Do you need to pass any extra context variables to the template?
    # Answer: Yes, we are passing Course Object (as dictionary) along with topics list,
    # so that we can get all the courses listed in that topic


# place order view
def place_order(request):
    msg = ''
    courlist = Course.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if order.levels <= order.course.stages:
                if (order.course.price > 150.00):
                    Course.discount(order.course)
                order.save()
                msg = 'Your course has been ordered successfully.'
            else:
                msg = 'You exceeded the number of levels for this course.'
            return render(request, 'myapp/order_response.html', {'msg': msg})
    else:
        form = OrderForm()
    return render(request, 'myapp/placeorder.html', {'form': form, 'msg': msg, 'courlist': courlist})

def coursedetail(request, cour_id):
    cour = Course.objects.get(pk=cour_id)
    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            if form['interested'].value() == '1':
                Course.objects.filter(pk=cour_id).update(interested = cour.interested + 1)
        return redirect('myapp:index')
    else:
        form = InterestForm()
    return render(request, 'myapp/coursedetail.html', {'cour': cour, 'InterestForm': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                # For Last Login
                response = HttpResponseRedirect(reverse('myapp:index'))
                print('Hello')
                if 'last_login' in request.COOKIES:
                    last_login = request.COOKIES['last_login']
                    # the cookie is a string - convert back to a datetime type
                    last_login_time = datetime.strptime(last_login[:-7], "%Y-%m-%d %H:%M:%S")
                    curr_time = datetime.now()
                    if (curr_time - last_login_time).days > 0:
                        response.set_cookie('last_login', datetime.now(),max_age=3600) # 1 hours Expiry
                    response = HttpResponseRedirect(reverse('myapp:myaccount/request.user.id'))
                else:
                    response.set_cookie('last_login', datetime.now(),max_age=3600) # 1 hours Expiry
                return response
                #return HttpResponseRedirect(reverse('myapp:index'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html')

@login_required
def user_logout(request):
    #logout(request)
    response = HttpResponseRedirect(reverse(('myapp:index')))
    response.delete_cookie('last_login')
    response.delete_cookie('sessionid')
    return response

def myaccount(request, st_id):
    if st_id != 0:
        try:
            if Student.objects.get(pk=st_id):
                if request.user.id == st_id:
                    user = get_object_or_404(Student, pk=st_id)
                    interested = Student.objects.filter(id=st_id).values_list('interested_in__courses__name',flat=True)
                    stud_course = Order.objects.filter(Student_id=st_id).values_list('course__name', flat=True)
                    return render(request,'myapp/myaccount.html', {'user': user, 'interested': interested, 'stud_course':stud_course})
                else:
                    msg = 'You are not a login user'
                    return render(request, 'myapp/order_response.html', {'msg': msg})
        except:
            msg = 'You are not a registered student'
            return render(request, 'myapp/order_response.html', {'msg': msg})
    else:
        return render(request, 'myapp/login.html')



def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                print('found it')
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request,'myapp/registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})

