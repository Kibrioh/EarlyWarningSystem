from django.urls import path
from .views import user_data_form, success_page, load_counties, load_sub_counties, load_locations, load_sub_locations
from .forms import UserDataForm
from . import views
from . import forms


urlpatterns = [
    path('', views.user_data_form, name='user_data_form'),
    path('success_page/', views.success_page, name='success_page'),
    path('load_counties/', views.load_counties, name='load_counties'),
    path('load_sub-counties/', views.load_sub_counties, name='load_sub_counties'),
    path('load_locations/', views.load_locations, name='load_locations'),
    path('load_sub_locations/', views.load_sub_locations, name='load_sub_locations'),
    path('save_user_data/', views.save_user_data, name='save_user_data'),
    path('save_user_data/', views.user_data_form, name='save_user_data'),
]

