from django.db import models
from django.db.models import OuterRef, Exists
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ..filters import RecipeFilter, IngredientFilter
from recipes.models import (
    Favorite,
    Ingredient,
    Recipe,
    ShoppingCart,
    Tag
)
from ..serializers.recipes import (
    FavoriteSerializer,
    IngredientSerializer,
    RecipeGETSerializer,
    RecipeCreateSerializer,
    ShoppingCartSerializer,
    TagSerializer
)
from ..services import get_shopping_list


class TagsModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = None


class IngredientsModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = None
    filter_backends = [IngredientFilter, ]
    search_fields = ['^name', ]


class RecipeModelViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filterset_class = RecipeFilter

    def get_queryset(self):
        queryset = (
            Recipe
            .objects
            .select_related('author')
            .prefetch_related('ingredients')
        )
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            favorited_subquery = Favorite.objects.filter(
                user=self.request.user,
                recipe=OuterRef('pk')
            )
            shopping_cart_subquery = ShoppingCart.objects.filter(
                user=self.request.user,
                recipe=OuterRef('pk')
            )
            queryset = queryset.annotate(
                is_favorited=Exists(
                    favorited_subquery,
                    output_field=models.BooleanField()
                ),
                is_in_shopping_cart=Exists(
                    shopping_cart_subquery,
                    output_field=models.BooleanField()
                )
            )
            return queryset
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeGETSerializer
        return RecipeCreateSerializer

    def post_favorite_or_shopping_cart(self, request, serializer_class, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user

        serializer = serializer_class(
            data={
                'user': user.id,
                'recipe': recipe.id
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    @action(
        detail=True,
        methods=['post'],
        permission_classes=(permissions.IsAuthenticated,)
    )
    def favorite(self, request, pk):
        return self.post_favorite_or_shopping_cart(
            request,
            FavoriteSerializer,
            pk
        )

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        recipe = self.get_object()
        user = request.user

        Favorite.objects.filter(
            user=user,
            recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        return self.post_favorite_or_shopping_cart(
            request,
            ShoppingCartSerializer,
            pk
        )

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        recipe = self.get_object()
        user = request.user

        ShoppingCart.objects.filter(
            user=user,
            recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=(permissions.IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        if not request.user.shopping_cart.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        file = f'{request.user.username}_shopping_list'
        response = get_shopping_list(request)
        response = FileResponse(response, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="{file}.txt"'
        return response
