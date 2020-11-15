from django.urls import path
from user_management import views as pages

urlpatterns = [
    path('', view=pages.AuthenticateUser.as_view(), name='login'),
    path('login/', view=pages.AuthenticateUser.as_view(), name='login'),
    path('dashboard/', view=pages.UserDashboard.as_view(), name='dashboard'),
    path('logout/', view=pages.logout, name='logout')
]
