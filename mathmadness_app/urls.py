"""Defines the URL patterns for the mathmadness_app."""

from django.urls import path

from . import views

app_name = 'mathmadness_app'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    # Page that shows all the categories
    path('categories/', views.categories, name='categories'),
    # Detail page for a single category / answering questions depending on the user
    path('categories/<int:category_id>/', views.category, name='category'),
    # Page for showing personal raport
    path('raport/', views.raport, name='raport'),
    # Page for adding new categories
    path('new_category/', views.new_category, name='new_category'),
    # Page for editing a category
    path('categories/<int:category_id>/edit_category', views.edit_category, name='edit_category'),
    # Page for adding new questions
    path('categories/<int:category_id>/new_question', views.new_question, name='new_question'),
    # Page that shows all math books
    path('books/', views.book, name='books'),
    # Page for reserving a book
    path('books/<int:book_id>/reserve', views.reserve, name='reserve'),
    # Page for returning a book
    path('books/<int:book_id>/return', views.return_book, name='return'),
    # Page for editing a book
    path('books/<int:book_id>/edit_book', views.edit_book, name='edit_book'),
    # Page for a single book
    path('books/<int:book_id>/', views.open_book, name='open_book'),
    # Page for adding a new book
    path('books/new_book', views.new_book, name='new_book'),
]