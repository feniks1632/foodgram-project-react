from django.contrib import admin

from .models import (
    Favorite,
    Ingredient,
    IngredientAmount,
    Recipe,
    ShoppingCart,
    Tag
)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'color',
        'slug'
    )
    empty_value_display = 'значение отсутствует'
    list_filter = ('name',)
    list_per_page = 10
    search_fields = ('name',)
    prepopulated_fields = {
        'slug': ('name',)
    }


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'measurement_unit'
    )
    empty_value_display = 'нет такого значения'
    list_filter = ('name',)
    list_per_page = 10
    search_fields = ('name',)


class IngredientAmountInline(admin.TabularInline):
    model = IngredientAmount
    min_num = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'author',
        'text',
        'get_tags',
        'get_ingredients',
        'cooking_time',
        'image',
        'pub_date',
        'count_favorite',
    )
    inlines = [
        IngredientAmountInline,
    ]

    empty_value_display = 'нет такого значения'
    list_editable = ('author',)
    list_filter = (
        'author',
        'name',
        'tags'
    )
    list_per_page = 10
    search_fields = (
        'author',
        'name'
    )

    def get_ingredients(self, object):
        return '\n'.join(
            (ingredient.name for ingredient in object.ingredients.all())
        )

    get_ingredients.short_description = 'ингредиенты'

    def get_tags(self, object):
        return '\n'.join((tag.name for tag in object.tags.all()))

    get_tags.short_description = 'теги'

    def count_favorite(self, object):
        return object.favorite.count()

    count_favorite.short_description = 'Количество добавлений в избранное'


@admin.register(IngredientAmount)
class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'ingredient',
        'amount',
        'recipe'
    )
    empty_value_display = 'нет такого значения'
    list_per_page = 10


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'recipe',
    )

    empty_value_display = 'нет такого значения'
    list_editable = (
        'user',
        'recipe'
    )
    list_filter = ('user',)
    search_fields = ('user',)
    list_per_page = 10


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'recipe',
    )

    empty_value_display = 'нет такого значения'
    list_editable = (
        'user',
        'recipe'
    )
    list_filter = ('user',)
    search_fields = ('user',)
    list_per_page = 10
