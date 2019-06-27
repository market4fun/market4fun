# users/admin.py
from django.contrib import admin,messages
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.db import models
from django.shortcuts import render,redirect

from django.http import HttpResponse,HttpResponseRedirect
from .models import Company, Stock,Quote,Order



admin.site.register(Company)
admin.site.register(Stock)
admin.site.register(Quote)
admin.site.register(Order)

