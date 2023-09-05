from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from typing import Set
from .models import Profile

admin.site.register(Profile)