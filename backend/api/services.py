import io


def get_shopping_list(ingredients):
    shopping_list = 'Нужно купить:'
    buffer = io.StringIO()
    buffer.write(f'{shopping_list}\n')
    for item in ingredients:
        buffer.write(f"{item['ingredient__name']} - ")
        buffer.write(f"{item['amount']}")
        buffer.write(f"{item['ingredient__measurement_unit']} \n")
    return buffer.getvalue()
