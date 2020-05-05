from django.contrib import admin

# Register your models here.

from .models import Author, Book, BookInstance, Review

class ReviewInline(admin.TabularInline):
    model = Review

class BooksInline(admin.TabularInline):
    model = Book

class BookInstanceInline(admin.TabularInline):
    model = BookInstance

class BookAdmin(admin.ModelAdmin):
    # fieldsets = [('Book', {'fields': ['title']}), ('')]
    list_display = ('title', 'author', 'publisher', 'year_of_publication', 'ISBN', 'status')
    inlines = [ReviewInline, BookInstanceInline]

class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back')
    list_display = ('book', 'status', 'due_back', 'id')
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BooksInline]

# admin.site.register(Author)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
# admin.site.register(BookInstance)

