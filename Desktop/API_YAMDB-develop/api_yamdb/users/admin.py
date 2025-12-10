from django.contrib import admin
from django.contrib.auth import get_user_model


User = get_user_model()


@admin.register(User)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email',
                    'role', 'bio', 'first_name', 'last_name')
