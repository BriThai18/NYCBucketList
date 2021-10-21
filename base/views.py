import contextlib
from typing import ContextManager
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .models import *
from .forms import EventForm, CustomerForm, CreateUserForm
from .decorator import admin_only, unauthenticated_user, allowed_users
from .filters import EventFilter

# Create your views here.
@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(user=user, name=user.username, email=user.email)
            return redirect('login')
    context = {'form': form}
    return render(request, 'base/register.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'base/login.html')

def logoutPage(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@admin_only
def home(request):
    events = Event.objects.all()
    customers = Customer.objects.all()

    total_customer = customers.count()
    total_events = events.count()
    
    context = {'events': events, 'customers': customers, 'total_customer': total_customer, 'total_events': total_events}

    return render(request, 'base/dashboard.html', context)

@login_required(login_url='login')
def customerHome(request):
    events = Event.objects.all()
    myFilter = EventFilter(request.GET, queryset=events)
    events = myFilter.qs
    context = {'myFilter': myFilter, 'events': events}
    return render(request, 'base/customerHome.html', context)

@login_required(login_url='login')
def customer(request, id):
    customer = Customer.objects.get(id=id)
    itinerary = customer.itinerary_set.all()
    context = {'customer': customer, 'itinerary': itinerary}
    return render(request, 'base/customer.html', context)

@login_required(login_url='login')
def updateCustomer(request, id):
    customer = Customer.objects.get(id=id)
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'base/updateCustomer.html', context)

@login_required(login_url='login')
def createEvent(request):
    form = EventForm()
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            form = EventForm()
    context = {'form': form}
    return render(request, 'base/createEvent.html', context)

@login_required(login_url='login')
def updateEvent(request, id):
    event = Event.objects.get(id=id)
    form = EventForm(instance=event)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'base/updateEvent.html', context)

@login_required(login_url='login')
def deleteEvent(request, id):
    event = Event.objects.get(id=id)
    if request.method == 'POST':
        event.delete()
        return redirect('/')
    context = {'event': event}
    return render(request, 'base/delete.html', context)

@login_required(login_url='login')
def cart(request):
    customer = Customer.objects.get(user=request.user)
    itinerary = customer.itinerary_set.all()
    context = {'itinerary': itinerary}
    return render(request, 'base/cart.html', context)

@login_required(login_url='login')
def deleteItinerary(request, id):
    itiner = Itinerary.objects.get(id=id)
    if request.method == 'POST':
        itiner.delete()
        return redirect('customerHome')
    context = {'itiner': itiner}
    return render(request, 'base/deleteItinerary.html', context)

@login_required(login_url='login')
def addItinerary(request, id):
    event = Event.objects.get(id=id)
    customer = Customer.objects.get(user=request.user)
    if request.method == 'POST':
        itinerary = Itinerary()
        itinerary.customer = customer
        itinerary.event = event
        itinerary.save()
        return redirect('customerHome')
    return render(request, 'base/addItinerary.html')

@login_required(login_url='login')
def viewEvent(request, id):
    event = Event.objects.get(id=id)
    context = {'event': event}
    return render(request, 'base/viewEvent.html', context)
