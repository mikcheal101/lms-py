from django.urls import path
from book_management import views as pages

urlpatterns = [
    path('', view=pages.BooksView.as_view()),
    path('<int:book_id>/', view=pages.BookView.as_view())
]
