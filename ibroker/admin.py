# users/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django import forms
from .models import Company, Stock,Quote,Order



admin.site.register(Company)
admin.site.register(Stock)
admin.site.register(Quote)
admin.site.register(Order)

