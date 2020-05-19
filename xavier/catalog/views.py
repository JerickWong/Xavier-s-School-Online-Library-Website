from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.

from catalog.models import Book, Author, BookInstance, Genre, Review

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
    paginate_by = 1

    context = {
        'book_list': book_list,
    }

    return render(request, 'book_list.html', context=context)

class BookListView(generic.ListView):
    model = Book
    paginate_by = 1
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

def book_detail_view(request, primary_key):
    try:
        book = Book.objects.get(pk=primary_key)
    except Book.DoesNotExist:
        raise Http404('Book does not exist')
    
    return render(request, 'catalog/book_detail.html', context={'book': book})

# alternatively
# from django.shortcuts import get_object_or_404

# def book_detail_view(request, primary_key):
#     book = get_object_or_404(Book, pk=primary_key)
#     return render(request, 'catalog/book_detail.html', context={'book': book})

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

    context = {
        'bookinstance': bookinstance,
        'booksreviewed': booksreviewed
    }

    return render(request, 'profile.html', context=context)


import datetime

from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
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
            return HttpResponseRedirect(reverse('index') )

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

            book_instance.borrower = request.user
            book_instance.due_back = form.cleaned_data['due_date']
            book_instance.status = 'r'
            book_instance.save()

            return HttpResponseRedirect(reverse('profile'))
    
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

            return HttpResponseRedirect(reverse('books'))
    else:
        form = ReviewForm()
    context = {
        'form': form,
        'book': book,
    }

    return render(request, 'catalog/review_book.html', context)

# def sign_up(request):
#     book = get_object_or_404(Book, pk=pk)

#     if request.method == 'POST':
        
#         form = ReviewForm(request.POST)

#         if form.is_valid():

#             review_text = form.cleaned_data['review']
#             reviewer = request.user
#             review = Review(review=review_text, reviewer=reviewer)
#             review.save()
#             book.reviews.add(review)
#             book.save()

#             return HttpResponseRedirect(reverse('books'))
#     else:
#         form = ReviewForm()
#     context = {
#         'form': form,
#         'book': book,
#     }

#     return render(request, 'catalog/review_book.html', context)