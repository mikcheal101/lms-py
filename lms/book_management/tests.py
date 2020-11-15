import datetime as dt
from django.test import TestCase
from book_management.models import Book, Issue
from django.contrib.auth.models import User as Staff
from django.contrib.auth.models import User as Customer


class BookTest(TestCase):
    def setUp(self):
        self.price = 120.00
        self.genre = "folk tale".title()
        self.name = "harry potter".title()
        self.book = Book(
            price=self.price,
            genre=self.genre,
            name=self.name)
        self.book.save()

    def tearDown(self):
        self.book.delete()

    def test_read_book(self):
        self.assertEqual(self.name, "harry potter".title())
        self.assertEqual(self.price, 120.00)
        self.assertEqual(self.genre, "folk tale".title())

    def test_update_name(self):
        self.book.name = "new name".title()
        self.book.save()
        self.assertEqual(self.book.name, "new name".title())

    def test_update_price(self):
        self.book.price = 110.00
        self.book.save()
        self.assertEqual(self.book.price, 110.00)

    def test_update_genre(self):
        self.book.genre = "new genre".title()
        self.book.save()
        self.assertEqual(self.book.genre, "new genre".title())


class BookViewTest(TestCase):
    def setUp(self):
        self.price = 120.00
        self.genre = "folk tale".title()
        self.name = "harry potter".title()
        self.book = Book(
            price=self.price,
            genre=self.genre,
            name=self.name)
        self.book.save()

    def tearDown(self):
        self.book.delete()

    def test_no_book(self):
        response = self.client.get('/books/')
        self.assertEqual(response.data, {'books', []})

    def test_read_book(self):
        response = self.client.get(f'/books/{self.book.id}/')
        book = response.data['book']

        self.assertEqual(self.name, book.name)
        self.assertEqual(self.price, book.price)
        self.assertEqual(self.genre, book.genre)

    def test_update_name(self):
        book = dict(
            name="new name".title(),
            price=self.price,
            genre=self.genre)

        response = self.client.put(f'/books/{self.book.id}/', book)
        book = response.data['book']
        self.assertEqual(self.book.name, book.name)

    def test_update_price(self):
        book = dict(
            name=self.name,
            price=110.00,
            genre=self.genre)

        response = self.client.put(f'/books/{self.book.id}/', book)
        book = response.data['book']
        self.assertEqual(self.book.price, book.price)

    def test_update_genre(self):
        book = dict(
            name=self.name,
            price=self.price,
            genre="new genre".title())

        response = self.client.put(f'/books/{self.book.id}/', book)
        book = response.data['book']
        self.assertEqual(self.book.genre, book.genre)


class IssueTest(TestCase):
    def setUp(self):
        self.fine_per_day = 100.00

        self.staff = Staff.objects.create_user(
            username="staff00001",
            email="staff00001@mail.com",
            password="password101",
            is_staff=True,
            is_superuser=True,
            is_active=True)
        self.staff.save()

        self.customer = Customer.objects.create_user(
            username="mohammed",
            email="mohammed@mail.com",
            password="password101",
            is_active=True)
        self.customer.save()

        self.pre_book = Book.objects.create(
            price=120.00,
            genre="folk tale".title(),
            name="harry potter".title())
        self.post_book = Book.objects.create(
            price=150.00,
            genre="folk tale".title(),
            name="the story of mallam ilia".title())

        self.return_date = dt.date.today()
        self.issue_date = self.return_date - dt.timedelta(10)
        self.expected_date = self.issue_date + dt.timedelta(5)
        """ 5 days to return the book """

        self.fine = 0.00
        if self.return_date > self.expected_date:
            self.fine = (self.return_date - self.expected_date).days
        self.fine = self.fine_per_day * self.fine

        self.pre_issue = Issue.objects.create(
            book=self.pre_book,
            staff=self.staff,
            issue_date=self.issue_date,
            customer=self.customer,
            expected_date=self.expected_date)
        self.pre_issue.save()

        self.post_issue = Issue.objects.create(
            book=self.post_book,
            staff=self.staff,
            issue_date=self.issue_date,
            customer=self.customer,
            expected_date=self.expected_date)

        self.post_issue.close_issue(
            returned_date=self.return_date,
            fine_per_day=self.fine_per_day)
        self.post_issue.save()

    def tearDown(self):
        self.pre_book.delete()
        self.post_book.delete()
        self.staff.delete()
        self.customer.delete()
        self.pre_issue.delete()
        self.post_issue.delete()

    def test_read_pre_issue(self):
        self.assertEqual(self.pre_issue.book, self.pre_book)
        self.assertEqual(self.pre_issue.staff, self.staff)
        self.assertEqual(self.pre_issue.customer, self.customer)
        self.assertEqual(self.pre_issue.issue_date, self.issue_date)
        self.assertEqual(self.pre_issue.expected_date, self.expected_date)

    def test_read_post_issue(self):
        self.assertEqual(self.post_issue.book, self.post_book)
        self.assertEqual(self.post_issue.staff, self.staff)
        self.assertEqual(self.post_issue.customer, self.customer)
        self.assertEqual(self.post_issue.issue_date, self.issue_date)
        self.assertEqual(self.post_issue.expected_date, self.expected_date)
        self.assertEqual(self.post_issue.fine, self.fine)
        self.assertEqual(self.post_issue.return_date, self.return_date)

    def test_return_book(self):
        self.pre_issue.close_issue(
            fine_per_day=self.fine_per_day,
            returned_date=self.return_date)
        self.pre_issue.save()

        self.assertEqual(
            self.pre_issue.fine,
            self.fine)
        self.assertEqual(
            self.pre_issue.return_date,
            self.return_date)


class IssueViewTest(TestCase):
    def setUp(self):
        self.fine_per_day = 100.00

        self.staff = Staff.objects.create_user(
            username="staff00001",
            email="staff00001@mail.com",
            password="password101",
            is_staff=True,
            is_superuser=True,
            is_active=True)
        self.staff.save()

        self.customer = Customer.objects.create_user(
            username="mohammed",
            email="mohammed@mail.com",
            password="password101",
            is_active=True)
        self.customer.save()

        self.pre_book = Book.objects.create(
            price=120.00,
            genre="folk tale".title(),
            name="harry potter".title())
        self.post_book = Book.objects.create(
            price=150.00,
            genre="folk tale".title(),
            name="the story of mallam ilia".title())

        self.return_date = dt.date.today()
        self.issue_date = self.return_date - dt.timedelta(10)
        self.expected_date = self.issue_date + dt.timedelta(5)
        """ 5 days to return the book """

        self.fine = 0.00
        if self.return_date > self.expected_date:
            self.fine = (self.return_date - self.expected_date).days
        self.fine = self.fine_per_day * self.fine

    def tearDown(self):
        self.pre_book.delete()
        self.post_book.delete()
        self.staff.delete()
        self.customer.delete()
        self.pre_issue.delete()
        self.post_issue.delete()

    def test_list_no_lent_books(self):
        response = self.client.get('/issues/books/')
        self.assertEqual(response.data, {'issues': []})

    def test_issue_book(self):
        self.pre_issue = Issue.objects.create(
            book=self.pre_book,
            staff=self.staff,
            issue_date=self.issue_date,
            customer=self.customer,
            expected_date=self.expected_date)
        self.pre_issue.save()

        response = self.client.get(
            f'/issues/books/issued/{self.pre_issue.id}/')
        issue = response.data['issue']

        self.assertEqual(self.pre_book, issue.book)
        self.assertEqual(self.staff, issue.staff)
        self.assertEqual(self.issue_date, issue.issue_date)
        self.assertEqual(self.customer, issue.customer)
        self.assertEqual(self.expected_date, issue.expected_date)

    def test_return_book(self):
        self.post_issue = Issue.objects.create(
            book=self.post_book,
            staff=self.staff,
            issue_date=self.issue_date,
            customer=self.customer,
            expected_date=self.expected_date)

        self.post_issue.close_issue(
            returned_date=self.return_date,
            fine_per_day=self.fine_per_day)
        self.post_issue.save()

        response = self.client.get(
            f'/issues/books/returned/{self.post_issue.id}/')
        issue = response.data['issue']

        self.assertEqual(self.pre_book, issue.book)
        self.assertEqual(self.staff, issue.staff)
        self.assertEqual(self.issue_date, issue.issue_date)
        self.assertEqual(self.customer, issue.customer)
        self.assertEqual(self.expected_date, issue.expected_date)
        self.assertEqual(self.return_date, issue.returned_date)
        self.assertEqual(self.fine, issue.fine)
