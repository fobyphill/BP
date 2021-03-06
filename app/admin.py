from django.contrib import admin
from app.models import Item, Supplier, Category, UserAccount, Transfer, UserPainInformation, ClientManager


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    pass


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    pass

def set_active_user(modeladmin, request, queryset):
    queryset.update(is_active=True)

set_active_user.short_description = "Сделать активными"

def set_passive_user(modeladmin, request, queryset):
    queryset.update(is_active=False)

set_passive_user.short_description = "Сделать неактивными"

class UserPainInline(admin.StackedInline):
    model = UserPainInformation
    #fields = ('inn')

class ListAdmin(admin.ModelAdmin):
    inlines = [UserPainInline, ]
    list_display = ['first_name', 'last_name', 'is_active']
    ordering = ['is_active']
    list_filter = ('is_active',)
    actions = [set_active_user, set_passive_user]
    search_fields = ['first_name', 'last_name', ]
    exclude = ('password', 'last_login', 'is_superuser', 'is_staf', 'Groups')
    # fields = ('UserName', 'first_name', 'last_name', 'email', 'manager_id')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["first_name"].label = "Имя пользователя"
        return form

admin.site.register(UserAccount, ListAdmin)

class AdminClinentManager(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', ]


admin.site.register(ClientManager, AdminClinentManager)

# class ListTransfer(admin.ModelAdmin):
#     list_display = ['id', 'modified_date', 'user_id', 'status_id']
#     ordering = ['status_id']
#     list_filter = ('status_id',)
#     search_fields = ['id', 'user_id']
#
# admin.site.register(Transfer, ListTransfer)