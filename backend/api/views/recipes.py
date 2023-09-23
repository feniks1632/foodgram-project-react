from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ..filters import IngredientSearchFilter, RecipeFilter
from ..serializers.recipes import (
    FavoriteSerializer,
    IngredientSerializer,
    RecipeGETSerializer,
    RecipeCreateSerializer,
    ShoppingCartSerializer,
    TagSerializer
)
from recipes.models import (
    Favorite,
    Ingredient,
    IngredientAmount,
    Recipe,
    ShoppingCart,
    Tag
)


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
    filterset_class = IngredientSearchFilter


class RecipeModelViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeGETSerializer
        return RecipeCreateSerializer

    @action(
        detail=False,
        methods=['post', 'delete'],
        url_path=r'(?P<pk>[\d]+)/favorite',
        url_name='favorite',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        if request.method == 'POST':
            serializer = FavoriteSerializer(
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

        elif request.method == 'DELETE':
            Favorite.objects.filter(
                user=user,
                recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'Рецепт не в избранном!'},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=(permissions.IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        if request.method == 'POST':
            serializer = ShoppingCartSerializer(
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
        elif request.method == 'DELETE':
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
        user = request.user
        ingredients = IngredientAmount.objects.filter(
            recipe__shopping_cart__user=user
        ).order_by('ingredient__name').values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))
        shopping_list = 'Нужно купить:'
        for ingredient in ingredients:
            shopping_list += (
                f"\n{ingredient['ingredient__name']} "
                f"({ingredient['ingredient__measurement_unit']}) - "
                f"{ingredient['amount']}")
        file = f'{user.username}_shopping_list'
        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="{file}.txt"'
        return response
