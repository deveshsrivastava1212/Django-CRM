from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Records

# Create your views here.
def home(request):
    records = Records.objects.all()

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        #Authenticate user
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In !")
            return redirect('home')
        else:
            messages.success(request, "There Was An Error Logging In, Please Try Again....")
            return redirect('home')

    else:
        return render (request, 'home.html', {'records':records})


# Logout the user

def logout_user(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out Successfully !")
    return redirect('home')


# Register the user

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            #Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password= password)
            login(request, user)
            messages.success(request, "You Have Successfully Registered")
            return redirect('home')
        
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form':form})
    
    return render(request, 'register.html', {'form':form})


# Customer record  view

def customer_record(request,pk):
    if request.user.is_authenticated:
        #look up the records
        customer_record = Records.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record':customer_record})
    else:
        messages.success(request, "You Must Be Logged In To View That Page ")
        return redirect('home')


#Delete the Record

def delete_record(request,pk):
    if request.user.is_authenticated:
        delete_it = Records.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Records Deleted Successfully")
        return redirect('home')
    else:
        messages.success(request, "You Must Be Logged In To Delete...")
        return redirect('home')


#Add record API

def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record Added Successfully....")
                return redirect('home')
        return render(request, 'add_record.html', {'form':form})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')


#update the record

def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Records.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request,"Record Updated Successfully...")
            return redirect('home')
        return render(request, 'update_record.html', {'form':form})
    else:
        messages.success(request,"You Must Be Logged In...")
        return redirect('home')
