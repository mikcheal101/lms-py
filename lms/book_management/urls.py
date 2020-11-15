from django.urls import path
from book_management import views as pages

urlpatterns = [
    path(
        '',
        view=pages.BooksView.as_view(),
        name='view-books'),
    path(
        'new-book/',
        view=pages.AddBookView.as_view(),
        name='add-book'),
    path(
        'issue-book/',
        view=pages.IssueBookView.as_view(),
        name='issue-book'),
    path(
        'view-issued-books/',
        view=pages.IssuedBooksView.as_view(),
        name='view-issued-books'),
    path(
        'return-book/<int:pk>/',
        view=pages.ReturnBookView.as_view(),
        name='return-book'),

    path(
        'update/<int:book_id>/',
        view=pages.UpdateBookView.as_view(),
        name='view-book'),
    path(
        'view/<int:book_id>/',
        view=pages.BookView.as_view(),
        name='view-book'),
]
