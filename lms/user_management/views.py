from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from user_management.forms import SigninForm
from django.views import View


class AuthenticateUser(View):

    def get(self, request):
        template = loader.get_template('users/login.html')
        login_form = SigninForm()
        context = dict(login_form=login_form)
        return HttpResponse(template.render(context, request))

    def post(self, request):
        login_form = SigninForm(request.POST)
        if login_form.is_valid():
            return HttpResponseRedirect('/dashboard/')
        else:
            template = loader.get_template('users/login.html')
            context = dict(login_form=login_form)
            return HttpResponse(template.render(context, request))


def logout(request):
    pass


def create_user(request):
    pass


def delete_user(request):
    pass


def add_book(request):
    pass


def add_issue(request):
    pass


def delete_book(request):
    pass


def delete_issue(request):
    pass


def update_book(request):
    pass


def update_issue(request):
    pass
