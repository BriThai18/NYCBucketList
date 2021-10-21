from django.urls import path
from django.urls.resolvers import URLPattern
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('customer/<int:id>', views.customer, name='customer'),
    path('updateCustomer/<int:id>', views.updateCustomer, name='updateCustomer'),
    path('createEvent/', views.createEvent, name='createEvent'),
    path('updateEvent/<int:id>', views.updateEvent, name='updateEvent'),
    path('deleteEvent/<int:id>', views.deleteEvent, name='deleteEvent'),
    path('login/',  views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('customerHome/', views.customerHome, name='customerHome'),
    path('cart/', views.cart, name='cart'),
    path('deleteItiner/<int:id>', views.deleteItinerary, name='deleteItiner'),
    path('addItiner/<int:id>', views.addItinerary, name='addItiner'),
    path('viewEvent/<int:id>', views.viewEvent, name='viewEvent'),
]