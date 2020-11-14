import datetime as dt
from django.test import TestCase
from book_management.models import Book, Issue
from django.contrib.auth.models import User as Customer


class UserTest(TestCase):
    def setUp(self):
        pass

    def test_can_login(self):
        pass

    def test_can_logout(self):
        pass


class AdminTest(TestCase):

    def setUp(self):
        pass

    def test_can_create_user(self):
        pass

    def test_can_delete_user(self):
        pass

    def test_can_add_book(self):
        pass

    def test_can_delete_book(self):
        pass

    def test_can_update_book(self):
        pass


class StaffTest(TestCase):
    def setUp(self):
        pass

    def test_can_lease_book(self):
        pass

    def test_can_return_book(self):
        pass


class BookTestCase(TestCase):
    def setUp(self):

        Customer.objects.create_user(
            email="calistus@samplemail.com",
            username="calistus",
            password="password101",
            is_active=True)
        """ create a sample customer """

        _ = [
            Book.objects.create(
                price=120.00,
                genre="history",
                name="sambisa books vol.{index}".title())
            for index, value in enumerate(range(1, 4))]
        """ create three sample books """

    def test_can_be_borrowed(self):
        """ test if book can be borrowed """

        customer = Customer.objects.get(username="calistus")
        book = Book.objects.get(pk=1)
        today = dt.date.today()
        issue_date = today - dt.timedelta(10)
        expected_date = issue_date + dt.timedelta(5)
        """ 5 days to return the book """

        issue = Issue.objects.create(
            customer=customer,
            book=book,
            issue_date=issue_date,
            expected_date=expected_date)

        self.assertFalse(issue is None)

    def test_can_be_returned(self):
        """ test if book can be borrowed """

        customer = Customer.objects.get(username="calistus")
        book = Book.objects.get(pk=1)
        return_date = dt.date.today()
        issue_date = return_date - dt.timedelta(10)
        expected_date = issue_date + dt.timedelta(5)
        """ 5 days to return the book """

        fine = 0.00
        if return_date > expected_date:
            fine = 100.00 * (return_date - expected_date).days

        issue = Issue.objects.create(
            customer=customer,
            book=book,
            issue_date=issue_date,
            return_date=return_date,
            expected_date=expected_date,
            fine=fine)

        self.assertEqual(issue.fine, 500.00)
