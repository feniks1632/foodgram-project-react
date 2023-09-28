import io

from django.db.models import Sum
from recipes.models import IngredientAmount


def get_shopping_list(request):
    user = request.user
    ingredients = IngredientAmount.objects.filter(
        recipe__shopping_cart__user=user
    ).order_by('ingredient__name').values(
        'ingredient__name',
        'ingredient__measurement_unit'
    ).annotate(amount=Sum('amount'))
    shopping_list = 'Нужно купить:'
    buffer = io.StringIO()
    buffer.write(f'{shopping_list}\n')
    for item in ingredients:
        buffer.write(f"{item['ingredient__name']} - ")
        buffer.write(f"{item['amount']}")
        buffer.write(f"{item['ingredient__measurement_unit']} \n")
    return buffer.getvalue()
