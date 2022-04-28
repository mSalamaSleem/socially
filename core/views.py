from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.dispatch import receiver
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from users_authentication.forms import *
from .forms import PostUpdateForm
from .models import *
from django.db.models.signals import post_save, post_delete, pre_save, pre_delete, m2m_changed


@method_decorator(login_required(login_url='login'), name='dispatch')
class HomeListView(ListView):
    model = Post
    template_name = 'home/home.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):  # responsible for items retrieve
        friends = []
        for friend in Friend.objects.filter(follower=self.request.user):
            friends.append(friend.followed)
        return Post.objects.filter(user__in=friends).order_by('-created_at')


@method_decorator(login_required(login_url='login'), name='dispatch')
class PostsListView(ListView):
    model = Post
    template_name = 'home/profile.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):  # responsible for items retrieve
        return Post.objects.filter(user=self.request.user).order_by('-created_at')


@method_decorator(login_required(login_url='login'), name='dispatch')
class PostsUpdateView(UpdateView):
    model = Post
    template_name = 'posts/update_post.html'
    form_class = PostUpdateForm
    success_url = reverse_lazy('profile')


@method_decorator(login_required(login_url='login'), name='dispatch')
class PostsDeleteView(DeleteView):
    model = Post
    template_name = 'posts/delete_post.html'
    success_url = reverse_lazy('profile')


@method_decorator(login_required(login_url='login'), name='dispatch')
class PostCreationView(CreateView):
    model = Post
    fields = ['caption']
    template_name = 'posts/new_post.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        number_of_posts = self.request.user.get_num_posts()
        if number_of_posts < 5:
            form.instance.user = self.request.user
            return super(PostCreationView, self).form_valid(form)
        else:
            if hasattr(self.request.user, 'customer'):
                if self.request.user.customer.ismember:
                    form.instance.user = self.request.user
                    return super(PostCreationView, self).form_valid(form)
            else:
                return redirect('membership_home')


@method_decorator(login_required(login_url='login'), name='dispatch')
class FriendProfileView(ListView):
    model = Post
    template_name = 'home/friend_profile.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get(self, *args, **kwargs):  # if search for same user redirect to profile
        friend_username = self.kwargs['username']
        authenticated_username = self.request.user.username
        if friend_username == authenticated_username:
            return redirect('profile')
        else:
            return super(FriendProfileView, self).get(*args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        friend = User.objects.get(username=self.kwargs['username'])
        context['friend'] = friend
        is_following = self.request.user.is_following(friend)
        context['is_following'] = is_following
        return context

    def get_queryset(self):  # responsible for items retrieve
        try:
            friend = User.objects.get(username=self.kwargs['username'])
        except User.DoesNotExist:
            raise Http404('OOPS no users found')
        return Post.objects.filter(user=friend).order_by('-created_at')


@method_decorator(login_required(login_url='login'), name='dispatch')
class SearchResult(ListView):
    model = User
    template_name = 'home/search_results.html'
    context_object_name = 'user_results'
    paginate_by = 5

    def get_queryset(self):
        return User.objects.filter(username__contains=self.request.GET['search_term']).order_by('username')


@login_required(login_url='login')
def follow_user(request, pk):
    followed = User.objects.get(pk=pk)
    new_friend = Friend(follower=request.user, followed=followed)
    new_friend.save()
    return redirect('friend-profile', username=followed.username)


@login_required(login_url='login')
def unfollow_user(request, pk):
    followed = User.objects.get(pk=pk)
    try:
        Friend.objects.filter(follower=request.user, followed=followed).delete()
    except Exception:
        # print(f"{new_friend.follower} following {new_friend.followed}")
        print('error delete')
    return redirect('friend-profile', username=followed.username)


@receiver(post_save, sender=Post)
def clear_cache(sender, instance, created, **kwargs):
    if instance.caption is not None:
        cache.clear()


@receiver(post_delete, sender=Post)
def clear_cache2(sender, instance, **kwargs):
    if instance.caption is not None:
        cache.clear()


# clear cache when friend is deleted or updated or created
@receiver(post_delete, sender=Friend)
def clear_cache3(sender, instance, **kwargs):
    cache.clear()


@receiver(post_save, sender=Friend)
def clear_cache4(sender, instance, **kwargs):
    cache.clear()

