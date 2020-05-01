from django.db import models
from django_mysql.models import ListTextField

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=200)

    # Many to Many Field because specs mentioned books can have more than 1 author
    author = models.ManyToManyField(Author, on_delete=models.SET_NULL, null=True)

    publisher = models.ForeignKey('Publisher', on_delete=models.SET_NULL, null=True)
    
    year_of_publication = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)

    ISBN = models.CharField('ISBN', max_length=13, help_text='13 Character ISBN number', null=True)
    status = models.BooleanField(
        max_length=1,
        choices=[
        ('A', 'Available'),
        ('R', 'Reserved')],
        default='A',
        help_text='Book Status'
    )

    # ListTextField is from mysql models. If theres a lot of complications, use ArrayField from PostgreSQL instead
    reviews = models.ListTextField(base_field=TextField(), size=10, help_text='Give a review of the book', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title


