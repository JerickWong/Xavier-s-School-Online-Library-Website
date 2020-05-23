from django.urls import path
from django.urls import include
from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    # path('catalog/', include('catalog.urls')),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    path('book/<uuid:pk>/borrow/', views.borrow_book, name='borrow'),
    path('book/<uuid:pk>/return/', views.return_book, name='return-book'),
    path('book/<int:pk>/review/', views.review_book, name='book-review'),
    path('accounts/signup/', views.sign_up, name='sign-up'),
    path('about/', views.about, name='about'),
    # url(r'^about', TemplateView.as_view(template_name='../catalog/templates/about_us.html'), name='about'),
    # (r'^about', 'django.views.generic.simple.direct_to_template', {'template': '../catalog/templates/about_us.html'}),
]

#Add URL maps to redirect the base URL to our application
from django.views.generic import RedirectView
urlpatterns += [
    path('', RedirectView.as_view(url='/catalog', permanent=False)),
]

# Use static() to add url mapping to serve static files during development (only)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

#Add Django site authentication urls (for login, logout, password management)

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]

urlpatterns += [   
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('profile/', views.profile, name='profile'),
]