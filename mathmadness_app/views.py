from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from .models import Category, Raport, Book
from django.shortcuts import render, redirect
from .forms import CategoryForm, QuestionForm, BookForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

#Valtteri
def index(request):
    """The home page for Math Madness"""
    return render(request, 'mathmadness_app/index.html')

#Valtteri
@login_required
def categories(request):
    """Show all categories."""
    categories = Category.objects.order_by('difficulty')
    context = {'categories': categories}
    return render(request, 'mathmadness_app/categories.html', context)

#Valtteri (Riko muokkasi nimen)
@login_required
def category_old(request, category_id):
    """Show a single category and all its questions."""
    category = Category.objects.get(id=category_id)
    questions = category.question_set.order_by('question_text')
    context = {'category': category, 'questions': questions}
    return render(request, 'mathmadness_app/category.html', context)

#Riko
@login_required
def category(request, category_id):
    """Show all questions as a form. (All form logic is in template)"""
    category = Category.objects.get(id=category_id)
    questions = category.question_set.order_by('question_text')
    correct_answers = 0
    if request.method == "POST":
        for question in questions:
            # Get the answer from the form and check if it is correct
            if question.answer == request.POST[f"{question.id}"]:
                correct_answers += 1
        new_answers = {
            "category": category.name,
            "difficulty": category.difficulty,
            "correct_answers": correct_answers,
            "wrong_answers": len(questions) - correct_answers,
            "total_questions": len(questions),
            "category_id": category.id
        }
        try:
            raport = Raport.objects.get(user=request.user)
            edit = False
            found = False
            for course in raport.raport:
                if course["category_id"] == category.id and new_answers["correct_answers"] > course["correct_answers"]:
                    edit = True
                    break
                elif course["category_id"] == category.id:
                    found = True
                    break
            if not found and not edit:
                raport.raport.append(new_answers)
                raport.save()
            elif edit:
                raport.raport = [i for i in raport.raport if not (i['category_id'] == category.id)]
                raport.raport.append(new_answers)
                raport.save()
        except ObjectDoesNotExist:
            raport = Raport(user=request.user, raport=[new_answers])
            raport.save()
        context = {'answers': f"You got {correct_answers} out of {len(questions)} correct!"}
        return render(request, 'mathmadness_app/answers.html', context)
    context = {'category': category, 'questions': questions}
    return render(request, 'mathmadness_app/category.html', context)

#Riko
@login_required
def raport(request):
    """Show the user's raport."""
    try:
        raport = Raport.objects.get(user=request.user)
        context = {'raport': raport.raport}
        return render(request, 'mathmadness_app/raport.html', context)
    except ObjectDoesNotExist:
        context = {'raport': []}
        return render(request, 'mathmadness_app/raport.html', context)

#Valtteri
@login_required
def new_category(request):
    
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = CategoryForm()
    else:
        # POST data submitted; process data.
        form = CategoryForm(data=request.POST)
        if form.is_valid():
            new_category = form.save(commit=False)
            new_category.creator = request.user
            new_category.save()
            return redirect('mathmadness_app:categories')

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'mathmadness_app/new_category.html', context)

# Tuomas
def edit_category(request, category_id):
    """Edit an existing book."""
    category = Category.objects.get(id=category_id)

    if request.method != 'POST':
    # Initial request; pre-fill form with the current review.
        form = CategoryForm(instance=category)
    else:
    # POST data submitted; process data.
        form = CategoryForm(instance=category, data=request.POST)
        if form.is_valid():
            messages.success(request, f"Category: {category} has been edited.")
            edit_category = form.save(commit=False)
            edit_category.save()
            return redirect('mathmadness_app:categories')
    context = {'category': category, 'form': form}
    return render(request, 'mathmadness_app/edit_category.html', context)

#Valtteri ja Tuomas
@login_required
def new_question(request, category_id):

    category = Category.objects.get(id=category_id)

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = QuestionForm()
    else:
        # POST data submitted; process data.
        form = QuestionForm(data=request.POST)
        if form.is_valid():
            new_question = form.save(commit=False)
            new_question.category = category
            print(new_question)
            print(new_question.category, new_question.question_text, new_question.answer)
            new_question.save()
            return redirect('mathmadness_app:categories')

    # Display a blank or invalid form.
    context = {'category': category,'form': form}
    return render(request, 'mathmadness_app/new_question.html', context)

# Tuomas
@login_required
def book(request):
    """Show all books."""
    books = Book.objects.order_by('date_added')
    reserved_books = Book.objects.filter(reserved=True, reserved_by=request.user)
    context = {'book': books, 'reserved_books': reserved_books}
    return render(request, 'mathmadness_app/book.html', context)

# Riko
@login_required
def reserve(request, book_id):
    """Reserve a book."""
    book = Book.objects.get(id=book_id)
    user = request.user
    if user.reserved_books.count() < 3:
        book.reserved = True
        book.reserved_by = user
        book.save()
        messages.success(request, f"Book {book} reserved!")
    else:
        messages.error(request, "You have already reserved 3 books.")
    return redirect('mathmadness_app:books')

# Riko
@login_required
def return_book(request, book_id):
    """Return a book."""
    book = Book.objects.get(id=book_id)
    book.reserved = False
    book.reserved_by = None
    book.save()
    messages.success(request, f"Book {book} returned.")
    return redirect('mathmadness_app:books')

#Tuomas
@login_required
def edit_book(request, book_id):
    """Edit an existing book."""
    book = Book.objects.get(id=book_id)

    if request.method != 'POST':
    # Initial request; pre-fill form with the current review.
        form = BookForm(instance=book)
    else:
    # POST data submitted; process data.
        form = BookForm(instance=book, data=request.POST)
        if form.is_valid():
            messages.success(request, f"Book: {book} has been edited.")
            edit_book = form.save(commit=False)
            edit_book.save()
            return redirect('mathmadness_app:books')
    context = {'book': book, 'form': form}
    return render(request, 'mathmadness_app/edit_book.html', context)

#Tuomas
@login_required
def open_book(request, book_id):
    """Show the content of a single book"""
    book = Book.objects.get(id=book_id)
    context = {'book': book}
    return render(request, 'mathmadness_app/open_book.html', context)

#Tuomas
@login_required
def new_book(request):
    """Add a new book."""
    if request.method != 'POST':
    # No data submitted; create a blank form.
        form = BookForm()
    else:
    # POST data submitted; process data.
        form = BookForm(data=request.POST)
        if form.is_valid():
            messages.success(request, f"Book: {book} has been added.")
            new_book = form.save(commit=False)
            new_book.save()
            return redirect('mathmadness_app:books')
    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'mathmadness_app/new_book.html', context)