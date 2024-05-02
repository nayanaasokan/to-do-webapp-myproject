from django.shortcuts import render,redirect
from django.views.generic import View
from todoapp.forms import TaskForm,RegistrationForm,LoginForm
from todoapp.models import Task
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.utils import timezone
from django.db.models import Count
from todoapp.decorator import signin_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views.decorators.cache import never_cache

# Create your views here.

# localhost:8000/todoapp/task/add/
# method:get,post

@method_decorator([signin_required,never_cache],name="dispatch")
class TaskCreateView(View):
    def get(self,request,*args,**kwargs):
        form=TaskForm()
        return render(request,"task_add.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=TaskForm(request.POST)
        if form.is_valid():
            form.instance.user_object=request.user
            form.save()
            messages.success(request,"task added successfully")
            return redirect("task-list")
        messages.error(request,"failed to add")
        return render(request,"task_add.html",{"form":form})
    
# url-localhost:8000/todoapp/task/all/
# method-get,post

@method_decorator([signin_required,never_cache],name="dispatch")
class TaskListView(View):
    def get(self,request,*args,**kwargs):
        qs=Task.objects.filter(user_object=request.user)
        cur_month=timezone.now().month
        cur_year=timezone.now().year
        group_by_qs=Task.objects.filter(
            user_object=request.user,
            date__month=cur_month,
            date__year=cur_year
            ).values("status").annotate(number=Count("status"))
        print(group_by_qs)
        return render(request,"task_list.html",{"data":qs,"status_count":group_by_qs})
    
# url-localhost:8000/todoapp/task/{id}
# method-get
    
@method_decorator([signin_required,never_cache],name="dispatch")
class TaskDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Task.objects.get(id=id)
        return render(request,"task_detail.html",{"data":qs})
    
# url-localhost:8000/todoapp/task/{id}/remove/
# method-get

@method_decorator([signin_required,never_cache],name="dispatch")
class TaskDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Task.objects.get(id=id).delete()
        messages.success(request,"one task deleted")
        return redirect("task-list")
    
# url-localhost:8000/todoapp/task/{id}/change/
# method-get,post

@method_decorator([signin_required,never_cache],name="dispatch")
class TaskUpdateView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        task_object=Task.objects.get(id=id)
        form=TaskForm(instance=task_object)
        return render(request,"task_edit.html",{"form":form})       
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        task_object=Task.objects.get(id=id)
        form=TaskForm(request.POST,instance=task_object)   
        if form.is_valid():
            form.save()
            messages.success(request,"task updated successfully")
            return redirect("task-list")
        messages.error(request,"failed to update")
        return render(request,"task_edit.html",{"form":form})


class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form=RegistrationForm()
        return render(request,"register.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            # data=form.cleaned_data
            # User.objects.create_user(**data)
            form.save()
            return redirect("signin")
        return render(request,"register.html",{"form":form})
    
class SignInView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"login.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            uname=data.get("username")
            pwd=data.get("password")
            user_object=authenticate(request,username=uname,password=pwd)
            if user_object:
                login(request,user_object)
                return redirect("task-list")
        return render(request,"login.html",{"form":form})


@method_decorator([signin_required,never_cache],name="dispatch")
class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")
    
    


