from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Follow


@admin.register(User)
class UsersAdmin(UserAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'role'
    )
    fieldsets = (
        (
            "User",
            {
                "fields":
                (
                    'username',
                    'password',
                    'email',
                    'first_name',
                    'last_name',
                    'role',
                    'last_login',
                    'date_joined'
                )
            }
        ),)
    search_fields = (
        'first_name',
        'email',
        'username'
    )
    list_filter = (
        'email',
        'first_name',
        'username'
    )
    actions = [
        'block_users',
        'unblock_users'
    ]

    def block_users(self, request, queryset):
        queryset.update(is_active=False)

    def unblock_users(self, request, queryset):
        queryset.update(is_active=True)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'author',
        'follow',
    )
    list_editable = (
        'author',
        'follow',
    )
    list_filter = ('author',)
    search_fields = ('author',)


admin.site.site_title = 'Админ-панель Foodgram'
admin.site.site_header = 'Админ-панель Foodgram'
