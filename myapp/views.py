from django.shortcuts import render,redirect
from django.views.generic import View
from myapp.models import Cakebox
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages


class CakeboxForm(forms.ModelForm):
    class Meta:
        model=Cakebox
        fields="__all__"
        widgets={
            "name":forms.TextInput(attrs={"class":"form-control"}),
            "flavour":forms.TextInput(attrs={"class":"form-control"}),
            "shape":forms.TextInput(attrs={"class":"form-control"}),
            "price":forms.NumberInput(attrs={"class":"form-control"}),
            "weight":forms.TextInput(attrs={"class":"form-control"}),
            "layer":forms.TextInput(attrs={"class":"form-control"}),
            "description":forms.Textarea(attrs={"class":"form-control","rows":5}),
            "pic":forms.FileInput(attrs={"class":"form-control"}),

        }

class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))



class RegistrationForm(UserCreationForm):

    password1=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))

    class Meta:
        model=User
        fields=["first_name","last_name","email","username","password1","password2"]    

        widgets={
            "first_name":forms.TextInput(attrs={"class":"form-control"}),
            "last_name":forms.TextInput(attrs={"class":"form-control"}),
            "email":forms.EmailInput(attrs={"class":"form-control"}),
            "username":forms.TextInput(attrs={"class":"form-control"}),
            "password1":forms.PasswordInput(attrs={"class":"form-control"}),
            "password2":forms.PasswordInput(attrs={"class":"form-control"})
        }


class CakeboxCreateView(View):
    def get(self,request,*args,**kwargs):
        form=CakeboxForm()
        return render(request,"cake-add.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=CakeboxForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            Cakebox.objects.create(**form.cleaned_data)
            return redirect("cake-list")
        return render(request,"cake-add.html",{"form":form})
    


class CakeboxListView(View):
    def get(self,request,*args,**kwargs):
        qs=Cakebox.objects.all()
        return render(request,"cake-list.html",{"cakes":qs})
    


class CakeboxDetailsView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Cakebox.objects.get(id=id)
        return render(request,"cake-detail.html",{"cake":qs})
    

class CakeboxDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Cakebox.objects.get(id=id).delete()
        return redirect("cake-list")   
    


class CakeboxEditView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        emp=Cakebox.objects.get(id=id)
        form=CakeboxForm(instance=emp)
        return render(request,"cake-edit.html",{"form":form})
    

    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        emp=Cakebox.objects.get(id=id)

        form=CakeboxForm(instance=emp,data=request.POST,files=request.FILES)

        if form.is_valid():

            form.save()
            return redirect("cake-detail",pk=id)
        return render(request,"cake-edit.html",{"form":form})
    



class SignUpView(View):

    def get(self,request,*args,**kwargs):
        form=RegistrationForm()
        return render(request,"register.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Account has been created successfully")
            return redirect("signin")
        messages.error(request,"Failed to created")
        return render(request,"register.html",{"form":form})
    

class SignInView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"login.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                messages.success(request,"Successfully")

            return redirect("cake-list")
        messages.error(request,"Invalid creadential")
        return render(request,"login.html",{"form":form})


def signout_view(request,*args,**kwargs):
    logout(request)
    return redirect("signin")