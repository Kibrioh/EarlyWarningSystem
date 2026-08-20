from django.contrib import admin
from .models import userdata, AdminBoundaries  
class UserDataAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'sub_location')
    list_filter = ('phone_number','sub_location')
    search_fields = ('first_name', 'last_name', 'phone_number', 'sub_location')
admin.site.register(userdata, UserDataAdmin)


class AdminBoundariesAdmin(admin.ModelAdmin):
 list_display = ('country','county','sub_cnty','sub_locat')
 search_fields = ('country','county','sub_cnty','sub_locat')
 filter_fields = ('country','county','sub_cnty','sub_locat')
admin.site.register(AdminBoundaries, AdminBoundariesAdmin)
