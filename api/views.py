from rest_framework import generics, permissions

from api.serializers import AllPostsSerializer
from core.models import Post, Friend


class PostsList(generics.ListAPIView):

    serializer_class = AllPostsSerializer

    def get_queryset(self):
        """
        This view should return a list of all the posts
        for the currently authenticated user.
        """
        currentuser = self.request.user
        friends = []
        for friend in Friend.objects.filter(follower=currentuser):
            friends.append(friend.followed)
        return Post.objects.filter(user__in=friends).order_by('-created_at')

    permission_classes = [permissions.IsAuthenticated]