from django.urls import path
from .views import user_data_form, success_page, load_counties, load_sub_counties, load_locations, load_sub_locations, save_user_data
from .forms import UserDataForm



urlpatterns = [
    path('', user_data_form, name='user_data_form'),
    path('load_counties/', load_counties, name='load_counties'),
    path('load_sub-counties/', load_sub_counties, name='load_sub_counties'),
    path('load_locations/', load_locations, name='load_locations'),
    path('load_sub_locations/', load_sub_locations, name='load_sub_locations'),
    path('save_user_data/', save_user_data, name='save_user_data'),
    path('success_page/', success_page, name='success_page'),
    ]

