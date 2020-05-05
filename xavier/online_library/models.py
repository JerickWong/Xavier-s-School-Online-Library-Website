from django.db import models
from django_mysql.models import ListTextField
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)

# Create your models here.

class User(AbstractBaseUser):

    # AbstractBaseUser has default password already

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, editable=False)
    id_number = models.CharField(max_length=8, editable=False, help_text="After your account has been created, it can never be edited.", default='N/A')
    REQUIRED_FIELDS = ['id_number'] # just when you craete a superuser, it will require you to input an id num

    # Boolean
    anonymous = models.BooleanField(default=False)
    student_teacher = models.BooleanField(default=True)
    book_manager = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    
    anonymous.hidden = student_teacher.hidden = book_manager.hidden = admin.hidden = True

    def __str__(self):
        return self.username
    
    def get_first_name(self):
        return self.first_name
    
    def get_last_name(self):
        return self.last_name
    
    def get_email(self):
        return self.email

    def get_full_name(self):
        return '%s %s' % (self.first_name, self.last_name)


class AccountManager(BaseUserManager):
    def create_account(self, email, first_name, last_name, username, password, role):
        
        def create_user(self, email, first_name, last_name, username, password, role):
            user = self.model(
                email = self.normalize_email(email)
            )
            user.set_password(password)
            user.first_name = first_name
            user.last_name = last_name
            user.username = username

            if role == 'Book Manager':
                user.student_teacher = False
                user.book_manager = True
            
            user.save(using=self._db)
            return user
        
        if not email:
            raise ValueError("Email address field is required")
        if not first_name:
            raise ValueError("First name field is required")
        if not last_name:
            raise ValueError("Last name field is required")
        if not username:
            raise ValueError("Username field is required")
        if not password:
            raise ValueError("Password field is required")
        if len(password) < 8 or (any(c.isalnum() for c in password)) or not (any(x.isupper() for x in password) and any(x.islower() for x in password)):
            raise ValueError("Password must be at least 8 characters long, contain at least one upper case, at least one lower case character, and a special character. Minimum of")
        
        return create_user(self, email, first_name, last_name, username, password, role)             
    

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

class Book(models.Model):
    title = models.CharField(max_length=200)

    # Many to Many Field because specs mentioned books can have more than 1 author
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True)

    publisher = models.CharField(max_length=32, null=True, blank=True)
    
    year_of_publication = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)

    ISBN = models.CharField('ISBN', max_length=13, help_text='13 Character ISBN number', null=True)
    status = models.CharField(
        max_length=1,
        choices=[
        ('A', 'Available'),
        ('R', 'Reserved')],
        default='A',
        help_text='Book Status'
    )

    # ListTextField is from mysql models. If theres a lot of complications, use ArrayField from PostgreSQL instead

    def __str__(self):
        return self.title

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    review_text = models.TextField(help_text='Write a review for this book')

    def __str__(self):
        return self.review_text

import uuid # Required for unique book instances

class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID')

    # if may problem, change Book Class to String 'Book'
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    
    LOAN_STATUS = (
        ('M', 'Maintenance'),
        ('O', 'On loan'),
        ('A', 'Available'),
        ('R', 'Reserved'),
    )
    
    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )
    
    class Meta:
        ordering = ['book']
        
    def __str__(self):
        return '%d %s' % (self.id, self.book.title)

# class Publisher(models.Model):
#     book = models.ForeignKey(Book, on_delete=models.SET_NULL)
#     name = models.CharField(max_length=32)

#     def __str__(self):
#         return self.name

