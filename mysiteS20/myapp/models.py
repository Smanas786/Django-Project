from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_range(value):
    if value < 100 or value > 200:
        raise ValidationError(
            _('%(value)s is not in range of 100 to 200'),
            params={'value': value},
        )

# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=200, blank=True)
    def __str__(self):
        return self.name

class Course(models.Model):
    topic = models.ForeignKey(Topic, related_name='courses', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_range])
    for_everyone = models.BooleanField(default=True)
    description = models.TextField(max_length=300, null=True, blank=True)
    #Lab7 Fields Added
    interested = models.PositiveIntegerField(default=0)
    stages = models.PositiveIntegerField(default=3)
    #Final Project
    hours = models.IntegerField(default=1)
    def __str__(self):
        return self.name

    def __float__(self):
        return self.price

    def discount(self):
        return (float(self.price) * 0.9)

class Student(User):
    CITY_CHOICES = [('WS', 'Windsor'),
        ('CG', 'Calgery'),
        ('MR', 'Montreal'),
        ('VC', 'Vancouver')]
    school = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=2, choices=CITY_CHOICES, default='WS')
    interested_in = models.ManyToManyField(Topic)
    def __str__(self):
        return self.first_name + " " + self.last_name

class Order(models.Model):
    ORDER_STATUS_CHOICES = [(0, 'Cancelled'), (1, 'Order Confirmed')]
    course = models.ForeignKey(Course, related_name='course', on_delete=models.CASCADE)
    Student = models.ForeignKey(Student, related_name='Student', on_delete=models.CASCADE, max_length=200)
    levels = models.PositiveIntegerField()
    order_status = models.IntegerField(choices=ORDER_STATUS_CHOICES, default=1)
    order_date = models.DateField(default=datetime.date.today)

    def total_cost(self):
        total = 0
        for item in self.course.all():
            if Course.__str__(item):
                total += Course.__float__(item)
        return str(total)

    def __str__(self):
        return str(self.course)


class UserProfileInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)
    def __str__(self):
        return self.user.username