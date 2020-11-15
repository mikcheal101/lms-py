from django.contrib.auth.models import User as Customer
from django.contrib.auth.models import User as Staff
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import View
from django.views.generic.edit import CreateView

from user_management.forms import (CreateCustomerForm, CreateStaffForm,
                                   SigninForm)


class AuthenticateUser(View):

    def get(self, request):
        template = loader.get_template('users/login.html')
        login_form = SigninForm()
        context = dict(login_form=login_form)
        return HttpResponse(template.render(context, request))

    def post(self, request):
        login_form = SigninForm(request.POST)
        if login_form.is_valid():
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            template = loader.get_template('users/login.html')
            context = dict(login_form=login_form)
            return HttpResponse(template.render(context, request))


class UserDashboard(View):
    def get(self,  request):
        template = loader.get_template('users/dashboard.html')
        context = dict()
        return HttpResponse(template.render(context, request))


class StaffList(View):
    def get(self, request):
        staff = Staff.objects.filter(
            is_active=True,
            is_staff=True)
        template = loader.get_template('staff/index.html')
        context = dict(staff=staff)
        return HttpResponse(template.render(context, request))


class CustomerList(View):
    def get(self, request):
        customers = Customer.objects.filter(
            is_active=True,
            is_staff=False,
            is_superuser=False)
        template = loader.get_template('customers/index.html')
        context = dict(customers=customers)
        return HttpResponse(template.render(context, request))


class CreateStaff(CreateView):
    template = loader.get_template('staff/add-staff.html')

    def get(self, request):
        staff_form = CreateStaffForm
        context = dict(staff_form=staff_form)
        return HttpResponse(self.template.render(context, request))

    def post(self,  request):
        staff_form = CreateStaffForm(request.POST)
        if staff_form.is_valid():
            staff_form.save()
            return HttpResponseRedirect(reverse('view-staff'))
        else:
            context = dict(staff_form=staff_form)
            return HttpResponse(self.template.render(context, request))


class CreateCustomer(View):
    template = loader.get_template('customers/add-customer.html')

    def get(self, request):
        customer_form = CreateCustomerForm
        context = dict(customer_form=customer_form)
        return HttpResponse(self.template.render(context, request))

    def post(self,  request):
        customer_form = CreateCustomerForm(request.POST)
        if customer_form.is_valid():
            customer_form.save()
            return HttpResponseRedirect(reverse('view-customers'))
        else:
            context = dict(customer_form=customer_form)
            return HttpResponse(self.template.render(context, request))


def logout(request):
    pass
