from django.urls import path
from user_management import views as pages

urlpatterns = [
    path(
        '',
        view=pages.AuthenticateUser.as_view(),
        name='login'),
    path(
        'login/',
        view=pages.AuthenticateUser.as_view(),
        name='login'),
    path(
        'dashboard/',
        view=pages.UserDashboard.as_view(),
        name='dashboard'),
    path(
        'new-staff/',
        view=pages.CreateStaff.as_view(),
        name='add-staff'),
    path(
        'all-staff/',
        view=pages.StaffList.as_view(),
        name='view-staff'),
    path(
        'new-customer/',
        view=pages.CreateCustomer.as_view(),
        name='add-customer'),
    path(
        'all-customers/',
        view=pages.CustomerList.as_view(),
        name='view-customers'),
    path(
        'logout/',
        view=pages.logout,
        name='logout')
]



