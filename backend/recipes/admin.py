from django.contrib import admin

from .models import (
    Tag,
    Ingredient,
    Recipe,
    IngredientAmount,
    Favorite,
    ShoppingCart
)


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit'
    )
    search_fields = ('^name',)
    list_filter = ('name',)


class IngredientAmountAdmin(admin.TabularInline):
    model = IngredientAmount
    fk_name = 'recipe'


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'name',
        'favorited'
    )
    list_filter = (
        'author',
        'name',
        'tags'
    )
    exclude = ('ingredients',)

    inlines = [
        IngredientAmountAdmin,
    ]

    def favorited(self, object):
        return Favorite.objects.filter(recipe=object).count()

    favorited.short_description = 'В избранном'


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag)
admin.site.register(Favorite)
admin.site.register(ShoppingCart)
admin.site.register(IngredientAmount)
