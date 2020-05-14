import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']
        
        # Check if a date is not in the past. 
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        # Check if a date is in the allowed range (+4 weeks from today).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        # Remember to always return the cleaned data.
        return data

class BorrowBookForm(forms.Form):
    due_date = forms.DateField(help_text='Enter return date')
    
    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']
        
        # Check if a date is not in the past. 
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        # Remember to always return the cleaned data.
        return data

class ReviewForm(forms.Form):
    review = forms.CharField(max_length=1000, help_text='Leave your review for this book')
    
    def clean_review(self):
        data = self.cleaned_data['review']

        if data == '':
            raise ValidationError(_('Do not leave this field empty'))

        return data

from django.contrib.auth.models import User

# class RegistrationForm(forms.Form):
#     first_name = forms.CharField(max_length=100, help_text="Enter your first name")
#     last_name = forms.CharField(max_length=100, help_text="Enter your last name")
#     username = forms.CharField(max_length=100, help_text='Enter a username (make sure that it is unique')
#     password = forms.CharField(widget=forms.PasswordInput)
#     confirm_password = forms.CharField(widget=forms.PasswordInput, help_text='Enter your password again')
#     email = forms.EmailField(help_text='Enter your email address')
#     id_num = forms.CharField(max_length=8, help_text="Enter your ID number")

#     selection = (
#         ('s', 'Student'),
#         ('t', 'Teacher'),
#     )

#     group = forms.CharField(choices=selection, default='s')

#     def clean_password(self):
#         data = self.cleaned_data['password']

#         if len(data) < 8:
#             raise ValidationError(_('Minimum field'))

#         return data

#     class Meta():
#         model = User
#         fields = ('username','password','email')