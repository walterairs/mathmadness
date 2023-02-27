from django import forms

from .models import *


class CategoryForm(forms.ModelForm):
    """Form for adding categories"""
    class Meta:
        model = Category
        fields = ['name', 'description', 'difficulty']
        labels = {'name': 'name', 'description': 'desc', 'difficulty': 'difficulty'}

class QuestionForm(forms.ModelForm):
    """Form for adding questions"""
    class Meta:
        model = Question
        fields = ['question_text', 'answer',]
        labels = {'question_text': 'question', 'answer': 'answer'}

class BookForm(forms.ModelForm):

    class Meta:

        model = Book
        fields = ['name', 'category', 'authors', 'year_published', 'content']
        labels = {'name': 'Name', 'category': 'Category', 'authors': 'Authors', 'year_published': 'Year published', 'content': 'Content'}