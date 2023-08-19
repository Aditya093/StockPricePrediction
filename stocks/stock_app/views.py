from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from .models import *
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import subprocess
import stocks.settings as settings
import os
# Create your views here.
#stocks\streamlit_app
def Register(request):
    form=CreateUseForm()
    if request.method=='POST':
        form=CreateUseForm(request.POST)
        if form.is_valid():
            user=form.save()
            username=form.cleaned_data.get('username')
            messages.success(request,'Account Successfully created for'+username)
            return redirect('login')
    context={'form':form}
    return render(request,'stock_app/register.html',context)

def Login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password,email=email)
        if user is not None:
            login(request,user)
            return redirect('forecast')
        else:
            messages.error(request,'Invalid Credentials')
            return redirect('login')
    context={}
    return render(request,'stock_app/login.html',context)    


@login_required
def logoutUser(request):
    logout(request)
    return redirect('login') 
def streamlit(request):
    command = [
        "streamlit", "run",
        ".\stock_app\streamlit_app\streamlit_app.py",
        "--server.port 8501",
        "--server.headless",
        "true"
        
    ]
    print(os.path.isfile(os.getcwd()+"\stock_app\streamlit_app\streamlit_app.py"))
    subprocess.run(" ".join(command),shell=True)
    context={}
    return render(request,'stock_app/forecast.html',context)
#stocks\stock_app\views.py