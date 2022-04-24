from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from .forms import *
from .models import User


class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'signup.html'

    # method 1
    def get_success_url(self):
        login(self.request, self.object)  # self.object is the user object
        return '/login'

    # method
    # def form_valid(self, form):
    #     user = form.save()
    #     login(self.request, user)
    #     return redirect('/login')

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('/')
        return super(SignUpView, self).get(*args, **kwargs)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('profile')
        else:
            print('username or password wrong')
            return redirect('login')


def logout_page(request):
    logout(request)
    return redirect('login')


@login_required(login_url='/login')
def profile(request):
    return render(request, 'profile.html')


@method_decorator(login_required(login_url='/login'), name='dispatch')
class ProfileSettingUpdateView(UpdateView):
    model = User
    form_class = ProfileSettingForm
    template_name = 'account_settings.html'
    success_url = '/'

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.request.user.pk)
