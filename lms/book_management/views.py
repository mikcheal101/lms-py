from book_management.models import Book
from book_management.forms import BookForm
from django.http import HttpResponse

from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView
from django.views import View


class BooksView(View):

    def get(self, request):
        output = Book.objects.all()
        return HttpResponse(output)

    def post(self, request):
        try:
            form = BookForm(request.data)
            if form.is_valid():
                form.save()
            return HttpResponse(form.data)
        except Exception:
            return HttpResponse(None)


class BookView(View):

    def get(self, request, book_id=None):
        pass

    def put(self, request, book_id=None):
        pass


# def books(request):
#     output = Book.objects.all()
#     return HttpResponse(output)


# def book(request, book_id=None):
#     try:
#         output = Book.objects.get(pk=book_id)
#         return HttpResponse(output)
#     except Exception:
#         return None


# def update_book(request, book_id):
#     try:
#         output = Book.objects.get(pk=book_id)
#         return HttpResponse(output)
#     except Exception:
#         return None
