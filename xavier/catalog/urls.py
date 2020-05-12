from django.urls import path
from django.urls import include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    # path('catalog/', include('catalog.urls')),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
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
    # path('accounts/login/', views.login, name='login'),
    # path('accounts/password_change/done/', views.pwchangedone, name='password_change_done'),
    # path('accounts/password_change/', views.pwchange, name='password_change'),
    # path('accounts/password_reset/', views.pwreset, name='password_reset'),
    # path('accounts/password_reset/done', views.pwresetdone, name='password_reset_done'),
    # path('accounts/reset/<uidb64>/<token>/', views.reset, name='password_reset_confirm'),
    # path('accounts/reset/done/', views.resetdone, name='password_reset_complete'),
]

# from django.conf.urls import url
# # from django.contrib.auth import views as auth_views
# from django.contrib.auth.views import login, logout

# urlpatterns += [
#     url(r'^accounts/login/$', login, name='login'),
#     url(r'^accounts/logout/$', logout, name='logout'),
# ]

urlpatterns += [   
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
]