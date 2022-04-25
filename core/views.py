from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from .forms import *
from .models import *


class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'auth/signup.html'

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
        return render(request, 'auth/login.html')
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


@method_decorator(login_required(login_url='/login'), name='dispatch')
class PostsListView(ListView):
    model = Post
    template_name = 'home/profile.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):  # responsible for items retrieve
        return Post.objects.filter(user=self.request.user).order_by('-created_at')


@method_decorator(login_required(login_url='/login'), name='dispatch')
class ProfileSettingUpdateView(UpdateView):
    model = User
    form_class = ProfileSettingForm
    template_name = 'home/account_settings.html'
    success_url = '/'

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.request.user.pk)


class PostCreationView(CreateView):
    model = Post
    fields = ['caption']
    template_name = 'posts/new_post.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(PostCreationView, self).form_valid(form)


@method_decorator(login_required(login_url='/login'), name='dispatch')
class FriendProfileView(ListView):
    model = Post
    template_name = 'home/friend_profile.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get(self, *args, **kwargs): # if search for same user redirect to profile
        friend_username = self.kwargs['username']
        authenticated_username = self.request.user.username
        if friend_username == authenticated_username:
            return redirect('/')
        else:
            return super(FriendProfileView, self).get(*args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        friend = User.objects.get(username=self.kwargs['username'])
        context['friend'] = friend
        return context

    def get_queryset(self):  # responsible for items retrieve
        friend = User.objects.get(username=self.kwargs['username'])
        return Post.objects.filter(user=friend).order_by('-created_at')


class SearchResult(ListView):
    model = User
    template_name = 'home/search_results.html'
    context_object_name = 'user_results'
    paginate_by = 5

    def get_queryset(self):
        return User.objects.filter(username__contains=self.request.GET['search-term'])
