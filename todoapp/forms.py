from django import forms
from todoapp.models import Task
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class TaskForm(forms.ModelForm):
    class Meta:
        model=Task
        exclude=("date","user_object",)
        widgets={
            "title":forms.TextInput(attrs={"class":"form-control"}),
            "status":forms.Select(attrs={"class":"form-control"}),
            "user":forms.TextInput(attrs={"class":"form-control"})
        }


# class RegistrationForm(forms.ModelForm):
#     class Meta:
#         model=User
#         fields=["username","password","email"]
#         widgets={
#             "username":forms.TextInput(attrs={"class":"form-control"}),
#             "password":forms.TextInput(attrs={"class":"form-control"}),
#             "email":forms.TextInput(attrs={"class":"form-control"})
#         }


class RegistrationForm(UserCreationForm):
    password1=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
    password2=forms.CharField(label="Confirm Password",widget=forms.PasswordInput(attrs={"class":"form-control"}))
    class Meta:
        model=User
        fields=["username","email","password1","password2"]
        widgets={
            "username":forms.TextInput(attrs={"class":"form-control"}),
            "email":forms.TextInput(attrs={"class":"form-control"})
        }
        labels={"password2":"confirm password",}

class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
