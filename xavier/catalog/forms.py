import datetime
import re

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

class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, help_text="Enter your first name")
    last_name = forms.CharField(max_length=100, help_text="Enter your last name")
    username = forms.CharField(max_length=100, help_text='Enter a username (make sure that it is unique)')
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput, help_text='Enter your password again')
    email = forms.EmailField(help_text='Enter your email address')
    id_num = forms.CharField(max_length=8, help_text="Enter your ID number")

    selection = (
        ('s', 'Student'),
        ('t', 'Teacher'),
    )

    group = forms.ChoiceField(choices=selection)
    # TODO put them in students/teachers group

    def clean_confirm_password(self):
        cleaned_data = super().clean()

        data = self.cleaned_data.get('password')
        data2 = self.cleaned_data.get('confirm_password')

        string_check= re.compile('[@_!#$%^&*()<>?/\|}{~:]')         

        rules = [lambda data: any(x.isupper() for x in data), # must have at least one uppercase
        lambda data: any(x.islower() for x in data),  # must have at least one lowercase
        lambda data: any(x.isdigit() for x in data),  # must have at least one digit
        lambda data: len(data) >= 8,                  # must be at least 8 characters
        lambda data: string_check.search(data) != None,  # must have at least one special character
        lambda data: data == data2,  # must be equal to the confirm password
        ]

        print(data, data2)

        if all(rule(data) for rule in rules):
            return data
        else:
            err = 'Password must have '

            if not any(x.isupper() for x in data):
                err += 'at least one uppercase, '
            if not any(x.islower() for x in data):
                err += 'at least one lowercase, '
            if not any(x.isdigit() for x in data):
                err += 'at least one number, '
            if not len(data) >= 8:
                err += 'at least 8 characters, '
            if string_check.search(data) == None:
                err += 'at least one special character, '
            if data != data2:
                err += 'and matches the confirm password'
            raise ValidationError (_(err))
        

    class Meta():
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'confirm_password', 'id_num')