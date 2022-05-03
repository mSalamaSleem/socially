from rest_framework import generics, permissions

from api.serializers import AllPostsSerializer, FriendsSerializer
from core.models import Post, Friend


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
