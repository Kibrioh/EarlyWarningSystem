from django.contrib import admin
from .models import UserData, AdminBoundaries  
class UserDataAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'opt_in_alerts', 'location')
    list_filter = ('opt_in_alerts', 'location')
    search_fields = ('first_name', 'last_name', 'phone_number', 'location')
admin.site.register(UserData, UserDataAdmin)


class AdminBoundariesAdmin(admin.ModelAdmin):
 list_display = ('country','county','sub_cnty','location','sub_locat')
 search_fields = ('country','county','sub_cnty','location','sub_locat')
 filter_fields = ('country','county','sub_cnty','location','sub_locat')
admin.site.register(AdminBoundaries, AdminBoundariesAdmin)
