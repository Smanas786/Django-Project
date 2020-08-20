
from django.urls import path, re_path
from myapp import views

app_name = 'myapp'

urlpatterns = [

    path(r'', views.index, name='index'),
    path(r'about/', views.about, name='about'),
    path(r'<int:top_no>', views.detail, name='top_no'),
    path(r'courses/', views.courses, name='courses'),
    path(r'place_order/', views.place_order, name='place_order'),
    path(r'courses/<int:cour_id>', views.coursedetail, name='coursedetail'),
    path(r'login/', views.user_login, name='user_login'),
    path(r'logout/', views.user_logout, name='user_logout'),
    path(r'myaccount/<int:st_id>', views.myaccount, name='myaccount'),
    path(r'register/', views.register, name='register'),



]

