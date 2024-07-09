from django.contrib import admin
from .models import Product, Category, Order, OrderLine, Review, UserInformation

# Register your models here.

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderLine)
admin.site.register(Review)
admin.site.register(UserInformation)

admin.site.site_header = "Bast Admin"
# Compare this snippet from project/app/views.py:
# from django.shortcuts import render, redirect
# from django.http import HttpResponse, HttpRequest
# from django.contrib.auth.models import User
# from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
# from django.contrib.auth.decorators import login_required
