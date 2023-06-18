from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import *

    
class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']



class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']




class FinanceForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')  #retrieve the request object
        super().__init__(*args, **kwargs)
        self.fields['customer'].initial = self.request.user

    class Meta:
        model = Finance
        fields = '__all__'
        
