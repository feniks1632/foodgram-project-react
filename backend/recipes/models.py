from django.core.validators import (
    MinValueValidator,
    RegexValidator
)
from django.db import models

from users.models import User


class Ingredient(models.Model):
    name = models.CharField(
        'Название ингридиента',
        blank=False,
        max_length=150,
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        blank=False,
        max_length=150,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Tag(models.Model):
    name = models.CharField(
        'Тег',
        max_length=50,
        unique=True,
        db_index=True,
    )
    color = models.CharField(
        'Цвет(HEX code)',
        max_length=7,
        unique=True,
        help_text='пример, #49B64E',
    )
    slug = models.SlugField(
        'Слаг',
        max_length=50,
        unique=True,
        help_text='уникальный адрес для тега',
        validators=[RegexValidator(
            regex=r'^[-a-zA-Z0-9_]+$',
            message='тег содержит недопустимый символ'
        )]
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.slug[:15]


class Recipe(models.Model):
    name = models.CharField(
        'Название рецепта',
        max_length=50,
        unique=True
    )
    image = models.ImageField(
        'Фото блюда',
        blank=True,
        upload_to='recipes/',
    )
    text = models.TextField(
        'Как готовить',
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
        help_text='введите время готовки в минутах',
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
    )
    amount = models.PositiveSmallIntegerField(
        'количество',
        validators=[
            MinValueValidator(
                1,
                message='Количество ингредиента не может быть меньше 1'
            ),
        ],
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Соответствие ингредиента и рецепта'
        verbose_name_plural = 'Таблица соответствия ингредиентов и рецептов'
        constraints = (
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient'
            ),
        )

    def __str__(self):
        return f'{self.recipe} содержит {self.ingredient}'


class Favorite(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='favorite',
    )
    user = models.ForeignKey(
        User,
        verbose_name='Добавленное пользователем в избранное',
        related_name='favorite',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'


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
