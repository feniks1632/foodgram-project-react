from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from ..serializers.users import (
    CustomUserSerializer,
    SubscribeSerializer
)
from users.models import (
    Subscribe,
    User
)


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=(permissions.IsAuthenticated,))
    def subscribe(self, request, id):
        author = get_object_or_404(User, id=id)
        follow = request.user

        if request.method == 'POST':
            serializer = SubscribeSerializer(
                author,
                data=request.data,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            Subscribe.objects.create(follow=follow, author=author)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        elif request.method == 'DELETE':
            Subscribe.objects.filter(
                follow=follow,
                author=author).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'],
            permission_classes=(permissions.IsAuthenticated,))
    def subscriptions(self, request):
        authors = User.objects.filter(author__follow=request.user)
        result_pages = self.paginate_queryset(authors)
        serializer = SubscribeSerializer(
            result_pages,
            many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
