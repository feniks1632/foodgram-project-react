from django.contrib import admin

from .models import User, Subscribe


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'first_name',
        'last_name'
    )
    list_display_links = ('id', )
    search_fields = (
        'email',
        'username'
    )
    list_filter = (
        'email',
        'username'
    )


admin.site.register(User, UserAdmin)
admin.site.register(Subscribe)
