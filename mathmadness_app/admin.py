from django.contrib import admin
from django.contrib.auth.models import User

# Register your models here.
from .models import Category, Question, Raport, Book

admin.site.register(Category)
admin.site.register(Question)
admin.site.register(Raport)
admin.site.register(Book)
