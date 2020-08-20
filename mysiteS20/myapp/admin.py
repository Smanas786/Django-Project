from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.db import models
from .models import Topic, Course, Student, Order, UserProfileInfo


def add_50_to_hours(modeladmin, request, queryset):
    for course in queryset:
        course.hours += 10
        course.save()

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'topic', 'price', 'hours', 'for_everyone']
    actions = [add_50_to_hours]

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['upper_case_name', 'city']

    def upper_case_name(self, obj):
        return ("%s %s" % (obj.first_name, obj.last_name)).upper()
    upper_case_name.short_description = 'Student Full Name'

# Register your models here.
admin.site.register(Topic)
#admin.site.register(Course)
#admin.site.register(Student)
admin.site.register(Order)
admin.site.register(UserProfileInfo)