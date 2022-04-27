from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy, reverse
from .forms import *

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes


class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'auth/signup.html'

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('profile')
        return super(SignUpView, self).get(*args, **kwargs)

    # method 1
    def get_success_url(self):
        login(self.request, self.object)  # self.object is the user object
        return reverse('login')

    # method
    # def form_valid(self, form):
    #     user = form.save()
    #     login(self.request, user)
    #     return redirect(reverse('login'))


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'GET':
        return render(request, 'auth/login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            print('username or password wrong')
            return redirect('login')


def logout_page(request):
    logout(request)
    return redirect('login')


@method_decorator(login_required(login_url='login'), name='dispatch')
class ProfileSettingUpdateView(UpdateView):
    model = User
    form_class = ProfileSettingForm
    template_name = 'auth/account_settings.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.request.user.pk)


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "auth/password/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="auth/password/password_reset.html",
                  context={"password_reset_form": password_reset_form})
