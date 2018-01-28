"""Module that generate HTML forms using Django"""
import re
from django import forms
from django.contrib.auth.models import User
from myapp.models import Profile

__author__="raghu"

class LoginForm(forms.Form):
    """Generate form with username and password fields."""
    username = forms.CharField(
        widget=forms.TextInput(attrs={'id':'username', 'type': 'text', 'class': 'form-control'}))
    password = forms.CharField(
        widget=forms.TextInput(attrs={'id':'password', 'type': 'password', 'class': 'form-control'}))

    def clean(self):
        """Raise exception when form data is invalid."""
        uname = self.cleaned_data['username']
        pwd = self.cleaned_data['password']

        if not User.objects.filter(username=uname).exists():
            self.add_error('username','Invalid Username')
        else:
            user = User.objects.get(username=uname)
            if pwd != user.password:
                self.add_error('password', 'Invalid Password')


    def save(self):
        """Store cleaned data into database."""
        data = self.cleaned_data
        user = User.objects.get(username=data['username'])
        return user

class UserForm(forms.Form):
    """Generate Registration form"""
    first_name = forms.CharField(widget=forms.TextInput(attrs={'id':'first_name','type': 'text', 'class': 'validate'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'id':'last_name','type': 'text', 'class': 'validate'}))
    #dob = forms.DateField(widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder':'DD/MM/YY'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'id':'email','type': 'email', 'class': 'validate'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'id':'username','type': 'text', 'class': 'validate'}))
    password = forms.CharField(widget=forms.TextInput(attrs={'id':'password1','type': 'password', 'class': 'validate'}))
    confirm_password = forms.CharField(widget=forms.TextInput(attrs={'id':'password2','type': 'password', 'class': 'validate'}))

    def clean(self):
        """Raise exceptions when form data is invalid."""
        uname = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password1 = self.cleaned_data['password']
        password2 = self.cleaned_data['confirm_password']

        if User.objects.filter(email=email).exists():
            self.add_error("email","Email already exists")

        if User.objects.filter(username=uname).exists():
            self.add_error("username","Username already exists")
        if not re.match('^\w+$', uname):
            self.add_error("username", "Username should be only alphanumeric")

        if password1 != password2:
            self.add_error("password","Passwords didn't match")

    def save(self):
        """Store cleaned data into database."""
        data = self.cleaned_data
        user = User(email=data['email'], first_name=data['first_name'],
                    last_name=data['last_name'], password=data['password'],
                    username=data['username'])
        user.save()
        profile = Profile(user=user)
        profile.save()
        return user