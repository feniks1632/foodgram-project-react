from django.urls import include, path
from rest_framework import routers

from .views.recipes import (
    IngredientsModelViewSet,
    RecipeModelViewSet,
    TagsModelViewSet,
)
from .views.users import (
    CustomUserViewSet

)

router = routers.DefaultRouter()
router.register('users', CustomUserViewSet, basename='users')
router.register('tags', TagsModelViewSet, basename='tags')
router.register('ingredients', IngredientsModelViewSet, basename='ingredients')
router.register('recipes', RecipeModelViewSet, basename='recipes')


urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]
