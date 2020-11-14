from django.test import TestCase
from django.contrib.auth.models import User as Staff
from django.contrib.auth.models import User as Customer
from django.contrib.auth import authenticate


class SigninTest(TestCase):
    def setUp(self):
        self.user = Staff.objects.create_user(
            username="sambo-hameed",
            password="password101",
            email="sambo-hameed@mail.com",
            is_staff=True,
            is_active=True)
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_correct(self):
        user = authenticate(
            username="sambo-hameed",
            password="password101")
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_wrong_username(self):
        user = authenticate(
            username="sambo-hamed",
            password="password101")
        self.assertFalse((user is not None) and user.is_authenticated)

    def test_wrong_password(self):
        user = authenticate(
            username="sambo-hameed",
            password="password10")
        self.assertFalse((user is not None) and user.is_authenticated)


class UserTest(TestCase):
    def setUp(self):
        pass

    def test_can_login(self):
        pass

    def test_can_logout(self):
        pass


class AdminTest(TestCase):

    def setUp(self):
        self.administrator = Staff.objects.create_user(
            username="sambo-hameed",
            password="password101",
            email="sambo-hameed@mail.com",
            is_staff=True,
            is_superuser=True,
            is_active=True)
        self.administrator.save()

    def test_can_create_user(self):
        user = dict(
            username="musa",
            email="musa@mail.com",
            password="password101",
            is_staff=True,
            is_active=True)

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


class SigninViewTest(TestCase):
    def setUp(self):
        self.user = Staff.objects.create_user(
            username="sambo-hameed",
            password="password101",
            email="sambo-hameed@mail.com",
            is_staff=True,
            is_active=True)
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_correct(self):
        payload = dict(username="sambo-hameed", password="password101")
        response = self.client.post(
            'authentication/login', payload)
        self.assertTrue(response.data['authenticated'])

    def test_wrong_username(self):
        payload = dict(username="sambo-hamed", password="password101")
        response = self.client.post(
            'authentication/login', payload)
        self.assertFalse(response.data['authenticated'])

    def test_wrong_password(self):
        payload = dict(username="sambo-hameed", password="password10")
        response = self.client.post(
            'authentication/login', payload)
        self.assertFalse(response.data['authenticated'])
