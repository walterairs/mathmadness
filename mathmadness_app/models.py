from django.db import models
from django.contrib.auth.models import User

#Valtteri
class Category(models.Model):
    """A category of questions"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    difficulty = models.IntegerField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        """Puts the categories in order of difficulty"""
        ordering = ['-difficulty']

    def __str__(self):
        """Return a string representation of the category"""
        return self.name

#Valtteri
class Question(models.Model):
    """A question that can be answered"""
    question_text = models.TextField()
    answer = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a string representation of the question"""
        return self.question_text

class Raport(models.Model):
    """A student's answers to a category."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    raport = models.JSONField()

    def __str__(self):
        """Return a string representation of the model."""
        return f"{self.user}'s raport"

class Book(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    authors = models.TextField()
    year_published = models.IntegerField()
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    reserved = models.BooleanField(default=False)
    reserved_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="reserved_books")

    def __str__(self):
        """Return a string representation of the model."""
        return f"{self.name}"
