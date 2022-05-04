from django.contrib.auth import authenticate
from django.db import IntegrityError
from django.http import Http404
from rest_framework import generics, permissions
from django.views.decorators.csrf import csrf_exempt

from api.serializers import AllPostsSerializer, FriendsSerializer, UserSerializer
from core.models import Post, Friend
from users_authentication.models import User
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from rest_framework.authtoken.models import Token


@csrf_exempt
def signup(request):
    try:
        if request.method == 'POST':
            data = JSONParser().parse(request)
            new_user = User.objects.create_user(username=data['username'], password=data['password'])
            new_user.save()
            token = Token.objects.create(user=new_user)
            return JsonResponse({'token': str(token)}, status=201)
    except IntegrityError:
        return JsonResponse({'error': 'user exist'}, status=404)


@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        user = authenticate(username=data['username'], password=data['password'])
        if user is None:
            return JsonResponse({'error': 'username or password incorrect'}, status=404)
        else:
            try:
                token = Token.objects.get(user=user)
            except Token.DoesNotExist:
                token = Token.objects.create(user=user)
        return JsonResponse({'token': str(token)}, status=200)


class SearchResultsList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        """
        This view should return a list of all user
        that contain keyword-search.
        """
        return User.objects.filter(username__contains=self.kwargs['key_to_search']).order_by('username')


class FriendsPostsList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AllPostsSerializer

    def get_queryset(self):
        """
        This view should return a list of all friends posts
        for the currently authenticated user.
        """
        currentuser = self.request.user
        friends = []
        for friend in Friend.objects.filter(follower=currentuser):
            friends.append(friend.followed)
        return Post.objects.filter(user__in=friends).order_by('-created_at')


class FriendsList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FriendsSerializer

    def get_queryset(self):
        """
        This view should return a list of all friends
        for the currently authenticated user.
        """
        return Friend.objects.filter(follower=self.request.user)


class FriendPostsList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AllPostsSerializer

    def get_queryset(self):
        """
        This view should return a list of all friends
        for the currently authenticated user.
        """
        return Post.objects.filter(user=self.kwargs['username']).order_by('-created_at')


class UserPostsList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AllPostsSerializer

    def get_queryset(self):
        """
        This view should return a list of all the posts
        for the currently authenticated user.
        """
        return Post.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserPostDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AllPostsSerializer

    def get_queryset(self):
        """
        This view should return an instance
        for the currently authenticated user.
        """
        return Post.objects.filter(user=self.request.user)


class Follow(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FriendsSerializer

    def perform_create(self, serializer):
        followed = User.objects.get(pk=self.kwargs['pk'])
        # new_friend = Friend(follower=self.request.user, followed=followed)
        # new_friend.save()
        serializer.save(follower=self.request.user, followed=followed)


class UnFollow(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FriendsSerializer

    def perform_create(self, serializer):
        followed = User.objects.get(pk=self.kwargs['pk'])
        try:
            Friend.objects.filter(follower=self.request.user, followed=followed).delete()
        except Friend.DoesNotExist:
            raise Http404('OOps dosn\'t exist')
