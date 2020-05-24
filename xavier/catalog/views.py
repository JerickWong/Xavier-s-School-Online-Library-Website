from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.utils.decorators import method_decorator
from catalog.forms import MyAuthenticationForm
from django.contrib.auth import REDIRECT_FIELD_NAME

# Create your views here.

from catalog.models import Book, Author, BookInstance, Genre, Review, BorrowedBefore

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    
    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    
    # The 'all()' is implied by default.    
    num_authors = Author.objects.count()
    
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

from django.views import generic
from django.contrib.auth.models import Permission

def bookListView(request):
    book_list = Book.objects.all()
    if request.user.is_authenticated:
        group_permissions = Permission.objects.filter(group__user=request.user)
    paginate_by = 5

    context = {
        'book_list': book_list,
    }

    return render(request, 'book_list.html', context=context)

class BookListView(generic.ListView):
    model = Book
    paginate_by = 5
    # context_object_name = 'home_book_list'   # your own name for the list as a template variable
    # queryset = Book.objects.filter(title__icontains='war')[:5] # Get 5 books containing the title war
    # template_name = 'catalog/home_book_list.html'  # Specify your own template name/location
    # def get_queryset(self):
    #     return Book.objects.filter(title__icontains='war')[:5] # Get 5 books containing the title war
    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get the context
    #     context = super(BookListView, self).get_context_data(**kwargs)
    #     # Create any data and add it to the context
    #     context['some_data'] = 'This is just some data'
    #     return context
    # Permissions that the user has via a group
    # def get_queryset(self):
    #     group_permissions = Permission.objects.filter(group__user=self.request.user)
    #     return Book.objects.filter()
    
    

class BookDetailView(generic.DetailView):
    model = Book

# alternatively
# from django.shortcuts import get_object_or_404

def book_detail_view(request, primary_key):
    book = get_object_or_404(Book, pk=primary_key)
    return render(request, 'catalog/book_detail.html', context={'book': book})

from django.contrib.auth.decorators import login_required

@login_required
def my_view(request):
    # You can do the same sort of thing manually by testing on request.user.is_authenticated, but the decorator is much more convenient!
    ...

from django.contrib.auth.mixins import LoginRequiredMixin

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10
    
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='r').order_by('due_back')

def profile(request):
    bookinstance = BookInstance.objects.all()
    booksreviewed = Book.objects.all()
    borrowedbefore = BorrowedBefore.objects.all()

    context = {
        'bookinstance': bookinstance,
        'booksreviewed': booksreviewed,
        'borrowedbefore': borrowedbefore
    }

    return render(request, 'profile.html', context=context)


import datetime

from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from catalog.forms import RenewBookForm

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return redirect('index')

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)


from catalog.forms import BorrowBookForm

def borrow_book(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':
        
        form = BorrowBookForm(request.POST)

        if form.is_valid():

            due_date = form.cleaned_data['due_date']
            book_instance.borrower = request.user
            book_instance.due_back = due_date
            book_instance.status = 'r'
            
            book_instance.save()

            return redirect('profile')
    
    else:
        form = BorrowBookForm(initial={'due_date': datetime.date.today()})

    context = {
        'form': form,
        'book_instance': book_instance
    }

    return render(request, 'catalog/borrow_book.html', context)


from catalog.forms import ReviewForm

def review_book(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        
        form = ReviewForm(request.POST)

        if form.is_valid():

            review_text = form.cleaned_data['review']
            reviewer = request.user
            review = Review(review=review_text, reviewer=reviewer)
            review.save()
            book.reviews.add(review)
            book.save()

            return redirect('books')
    else:
        form = ReviewForm()
    context = {
        'form': form,
        'book': book,
    }

    return render(request, 'catalog/review_book.html', context)


from catalog.forms import RegistrationForm
from django.contrib.auth import login, authenticate

def sign_up(request):

    if request.method == 'POST':
        
        form = RegistrationForm(request.POST)

        if form.is_valid():                        

            # Saving user to the database
            user = form.save()
            user.refresh_from_db()
            raw_password = form.cleaned_data.get('password')
            user.set_password(raw_password)
            user.save()

            # Automatically signing the user up
            raw_password = form.cleaned_data.get('password')
            # user = authenticate(username=user.username, password=raw_password)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            # Setting user to Student / Teacher Group
            group = Group.objects.get(name='Student/Teacher') 
            group.user_set.add(user)            
            
            return redirect('index')

    else:
        form = RegistrationForm(initial={'group': 's'})

    return render(request, 'registration/signup.html', {'form': form})

def return_book(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    book_instance.borrower = None
    book_instance.due_back = None
    book_instance.status = 'a'
    book = book_instance.book

    borrowed_before = BorrowedBefore(borrower=request.user, book=book)
    borrowed_before.save()

    book_instance.save()

    return render(request, 'catalog/return_successfully.html', {})

def about(request):
    return render(request, 'about.html', {})


from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache

@csrf_protect
@never_cache
def auth_login(request, template_name='registration/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=MyAuthenticationForm):
          pass

from django.contrib.auth.views import LoginView

class Login(LoginView):
    template_name = 'login.html'