from django.contrib import admin

from .models import CustomUser

class UserAdmin(admin.ModelAdmin):

    list_display = ('id','username', 'role',)

admin.site.register(CustomUser,UserAdmin)
