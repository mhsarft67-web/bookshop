from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserChangeForm , UserCreationForm
from django.contrib.auth.models import Group
from .models import User



class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ( 'phone_number' , 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None , {'fields': ('phone_number' , 'full_name' , 'password')}),
        ('permission' , {'fields' : ('is_admin' ,'is_active' , 'last_login' )}),
    )
    #baraye UserCreationForm
    add_fieldsets = (
        (None , {'fields' :( 'phone_number'  , 'full_name' , 'password1' , 'password2')}),
    )

    search_fields = ('full_name',)
    ordering = ('full_name',)
    filter_horizontal = ()


admin.site.unregister(Group)
admin.site.register(User , UserAdmin)



# Register your models here.
