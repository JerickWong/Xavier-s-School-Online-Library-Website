import datetime
import re

from django.contrib.auth.forms import AuthenticationForm
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
    first_name = forms.CharField(max_length=100, help_text="Enter your first name", widget=forms.TextInput(attrs={'class' : 'input'}))
    last_name = forms.CharField(max_length=100, help_text="Enter your last name", widget=forms.TextInput(attrs={'class' : 'input'}))
    username = forms.CharField(max_length=100, help_text='Enter a username (make sure that it is unique)', widget=forms.TextInput(attrs={'class' : 'input'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'input'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'input'}), help_text='Enter your password again')
    email = forms.EmailField(help_text='Enter your email address', widget=forms.TextInput(attrs={'class' : 'input'}))
    id_num = forms.CharField(max_length=8, help_text="Enter your ID number", widget=forms.TextInput(attrs={'class' : 'input'}))

    # selection = (
    #     ('s', 'Student'),
    #     ('t', 'Teacher'),
    # )

    # group = forms.ChoiceField(choices=selection)
    # TODO put them in students/teachers group

    def clean_id_num(self):
        cleaned_data = super().clean()

        data = self.cleaned_data.get('password')
        data2 = self.cleaned_data.get('confirm_password')
        data3 = self.cleaned_data.get('id_num')

        string_check= re.compile('[@_!#$%^&*()<>?/\|}{~:]')         

        rules = [lambda data: any(x.isupper() for x in data), # must have at least one uppercase
        lambda data: any(x.islower() for x in data),  # must have at least one lowercase
        lambda data: any(x.isdigit() for x in data),  # must have at least one digit
        lambda data: len(data) >= 8,                  # must be at least 8 characters
        lambda data: string_check.search(data) != None,  # must have at least one special character
        # lambda data: data == data2,  # must be equal to the confirm password
        ]        
        
        if not all(rule(data) for rule in rules):
            raise ValidationError(_('Password must have at least one uppercase, one lowercase and one special character with a minimum of 8 characters.'))            
        elif data != data2:
            raise ValidationError(_('Password and confirm password must match.'))
        if not data3.isdigit():
            raise ValidationError(_('Enter numbers only on the ID Number field.'))
        else:
            return data
            # err = 'Password must have at least '

            # if not any(x.isupper() for x in data):
            #     err += 'one uppercase, '
            # if not any(x.islower() for x in data):
            #     err += 'one lowercase, '
            # if not any(x.isdigit() for x in data):
            #     err += 'one number, '
            # if not len(data) >= 8:
            #     err += '8 characters, '
            # if string_check.search(data) == None:
            #     err += 'one special character, '
            # if data != data2:
            #     err += 'and matches the confirm password,'
            # raise ValidationError (_(err))
        

    class Meta():
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'confirm_password', 'id_num')

class MyAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label=_("Username"), max_length=30, widget=forms.TextInput(attrs={'class' : 'input'}))
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput(attrs={'class' : 'input'}))

    def __init__(self, *args, **kwargs):
        super(MyAuthenticationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'input'
    
    def confirm_login_allowed(self, user):
        if not user:
            raise forms.ValidationError(_('User does not exist'))
        elif not user.is_active or not user.is_validated:
            raise forms.ValidationError('There was a problem with your login.', code='invalid_login')