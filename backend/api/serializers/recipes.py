from django.db import transaction
from drf_extra_fields.fields import Base64ImageField

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import (
    Favorite,
    Ingredient,
    IngredientAmount,
    Recipe,
    ShoppingCart,
    Tag
)
from .users import UserSerializer


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit'
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug'
        )


class AddIngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientAmount
        fields = (
            'id',
            'amount'
        )


class IngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="ingredient.id")
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientAmount
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount'
        )


class RecipeCreateSerializer(serializers.ModelSerializer):
    ingredients = AddIngredientInRecipeSerializer(many=True)
    image = Base64ImageField()
    author = UserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time',
            'author'
        )

    def validate(self, ingredients):
        ingredients_data = ingredients.get("ingredients")
        ingredients_list = []
        for ingredient in ingredients_data:
            ingredient_id = ingredient['id']
            ingredients_list.append(ingredient_id)
        if len(set(ingredients_list)) != len(ingredients_list):
            raise serializers.ValidationError(
                'Ингредиенты не могут повторяться!'
            )
        return super().validate(ingredients)

    def add_ingredients(self, ingredients_data, recipe):
        IngredientAmount.objects.bulk_create([IngredientAmount(
            ingredient=ingredient['id'],
            recipe=recipe,
            amount=ingredient['amount']
        ) for ingredient in ingredients_data])

    @transaction.atomic
    def create(self, validated_data):
        request = self.context.get('request')
        tags_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(
            author=request.user,
            **validated_data
        )
        recipe.tags.set(tags_data)
        self.add_ingredients(
            ingredients_data,
            recipe
        )
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        tags = validated_data.pop(
            'tags',
            None
        )
        ingredients = validated_data.pop(
            'ingredients',
            None
        )
        recipe = super().update(
            instance,
            validated_data
        )
        if ingredients:
            recipe.ingredients.clear()
            self.add_ingredients(
                ingredients,
                recipe
            )
        if tags:
            recipe.tags.clear()
            recipe.tags.set(tags)
        return recipe

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeGETSerializer(
            instance,
            context=context).data


class RecipeGETSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    ingredients = IngredientAmountSerializer(
        many=True,
        source='IngredientAmount'
    )
    tags = TagSerializer(
        many=True,
        read_only=True
    )
    image = Base64ImageField()
    is_favorited = serializers.BooleanField(read_only=True)
    is_in_shopping_cart = serializers.BooleanField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )


class RecipeShortSerializer(serializers.ModelSerializer):
    image = Base64ImageField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = (
            'recipe',
            'user'
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=(
                    'recipe',
                    'user'
                ),
                message='Этот рецепт уже в избранном!'
            )
        ]

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        recipe = instance.recipe
        return RecipeShortSerializer(
            recipe,
            context=context).data


class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = (
            'recipe',
            'user'
        )
        validators = [
            UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=(
                    'recipe',
                    'user'
                ),
                message='Этот рецепт уже в списке покупок!'
            )
        ]

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        recipe = instance.recipe
        return RecipeShortSerializer(
            recipe,
            context=context).data
