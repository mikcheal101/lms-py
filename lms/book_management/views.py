from book_management.models import Book, Issue
from book_management.forms import BookForm, IssueForm,  ReturnBookForm
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from django.views import View
from django.urls import reverse
from django.views.generic import CreateView, UpdateView


class BooksView(View):

    def get(self, request):
        books = Book.objects.all()
        template = loader.get_template('books/books.html')
        context = dict(books=books)
        return HttpResponse(template.render(context, request))


class AddBookView(View):

    def get(self,  request):
        book_form = BookForm()
        template = loader.get_template('books/add-book.html')
        context = dict(book_form=book_form)
        return HttpResponse(template.render(context, request))

    def post(self, request):
        book_form = BookForm(request.POST)
        if book_form.is_valid():
            book_form.save()
            return HttpResponseRedirect(reverse('view-books'))
        else:
            template = loader.get_template('books/add-book.html')
            context = dict(book_form=book_form)
            return HttpResponse(template.render(context, request))


class IssueBookView(CreateView):
    model = Issue
    form_class = IssueForm
    template_name = 'books/issue-book.html'

    def post(self, request):
        form_class = IssueForm(request.POST)
        if form_class.is_valid():
            form_class.save()
            return HttpResponseRedirect(reverse('view-issued-books'))
        else:
            return HttpResponseRedirect(reverse('issue-book'))


class IssuedBooksView(View):
    def get(self,  request):
        rentals = Issue.objects.filter(return_date=None)
        context = dict(rentals=rentals)
        template = loader.get_template('books/issued-books.html')
        return HttpResponse(template.render(context, request))


class ReturnBookView(UpdateView):
    model = Issue
    form_class = ReturnBookForm
    template_name = 'books/return-book.html'

    def get_success_url(self):
        return reverse('view-issued-books')


class UpdateBookView(View):

    def put(self, request, book_id=None):
        book = Book.objects.none()
        book_form = BookForm()
        try:
            book = Book.objects.get(pk=book_id)
            book_form = BookForm(request.PUT, instance=book)
            if book_form.is_valid():
                book_form.save()
                return HttpResponseRedirect(reverse('view-books'))
        except Book.DoesNotExist:
            pass

        template = loader.get_template('books/book.html')
        context = dict(book_form=book_form)
        return HttpResponse(template.render(context, request))


class BookView(View):

    def get(self, request, book_id=None):
        book = Book.objects.none()
        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            pass

        template = None
        context = dict(book=book)
        return HttpResponse(template.render(context, request))
