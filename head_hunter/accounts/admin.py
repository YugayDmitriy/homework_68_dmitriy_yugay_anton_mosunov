from django.contrib import admin
from accounts.models import Account


class AccountAdmin(admin.ModelAdmin):
    list_display = ('user_category', 'username', 'email', 'phone', 'avatar', 'created_at', 'changed_at', )
    list_filter = ('user_category', 'username', 'email', 'phone', 'avatar', 'created_at', 'changed_at', )
    search_fields = ('user_category', 'username', 'email', 'phone', 'avatar', 'created_at', 'changed_at', )
    fields = ('user_category', 'username', 'email', 'phone', 'avatar', )
    readonly_fields = ['id']


admin.site.register(Account, AccountAdmin)
