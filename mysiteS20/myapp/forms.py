from django import forms
from myapp.models import Order, Student, UserProfileInfo
from django.contrib.auth.models import User

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['Student', 'course', 'levels', 'order_date']
        #widgets = {
        #    'Student': forms.RadioSelect(),
        #    'order_date': forms.SelectDateWidget(),
        #}
        student = forms.RadioSelect()
        order_date = forms.DateField(widget=forms.SelectDateWidget)


class InterestForm(forms.Form):
    interested = forms.ChoiceField(
        choices=[('1', 'Yes'), ('0', 'No')],
        widget=forms.RadioSelect)
    levels = forms.IntegerField(min_value=1, initial=1)
    comments = forms.CharField(widget=forms.Textarea, required=False, label="Additional Comments")

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username','password', 'first_name', 'last_name')


class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = Student
        fields = ('city', 'interested_in')
        model = UserProfileInfo
        fields = ('profile_pic',)


