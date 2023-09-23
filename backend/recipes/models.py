from django.core.validators import (
    MinValueValidator,
)
from django.db import models

from users.models import User


class Tag(models.Model):
    name = models.CharField(
        'Название тега',
        unique=True,
        max_length=200
    )
    color = models.CharField(
        'HEX цвета',
        unique=True,
        max_length=7,
    )
    slug = models.SlugField(
        'Слаг тега',
        unique=True,
        max_length=200
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        'Название ингридиента',
        max_length=150,
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=150,
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    name = models.CharField(
        'Название рецепта',
        max_length=200,
    )
    image = models.ImageField(
        'Фото',
        upload_to='recipes/',
    )
    text = models.TextField(
        'Описание рецепта'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингридиенты',
        through='IngredientAmount',
        related_name='recipes',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тег',
        related_name='recipes',
    )
    cooking_time = models.IntegerField(
        'Время готовки',
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        related_name='IngredientAmount',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        related_name='IngredientAmount',
        on_delete=models.CASCADE,
    )
    amount = models.PositiveSmallIntegerField(
        'Количество ингредиента',
        validators=[
            MinValueValidator(
                1,
                message='Количество ингредиента не может быть меньше 1'
            ),
        ],
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Связь ингредиента с рецептом'
        verbose_name_plural = 'Связь ингредиентов с рецептами'
        constraints = (
            models.UniqueConstraint(
                fields=[
                    'recipe',
                    'ingredient'
                ],
                name='unique_ingredient_in_recipe'
            ),
        )

    def __str__(self):
        return f'{self.recipe} содержит {self.ingredient}'


class Favorite(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт в избранном',
        on_delete=models.CASCADE,
        related_name='favorite',
    )
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='favorite',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'user',
                    'recipe'
                ],
                name='unique_favorite',
            )
        ]


class ShoppingCart(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Добавленное пользователем в список покупок',
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'user',
                    'recipe'
                ],
                name='unique_shopping_cart',
            )
        ]
