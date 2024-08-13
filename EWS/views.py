from random import choices
import traceback
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from EWS.forms import UserDataForm
from django.http import HttpResponse
from geopy.geocoders import Nominatim
from twilio.rest import Client
from EWS.models import userdata, AdminBoundaries
from django.conf import settings
import openpyxl
from django.views.decorators.http import require_POST
from django.db import transaction
# view functions

def load_counties(request):
    counties = AdminBoundaries.objects.order_by('county').distinct('county')
    counties_list = [{'county': 'Select county'}]  # Initial value
    counties_list += [{'county': c.county} for c in counties]
    return JsonResponse(counties_list, safe=False)

def load_sub_counties(request):
    county = request.GET.get('county')
    sub_counties = AdminBoundaries.objects.filter(county=county).order_by('sub_cnty').distinct('sub_cnty')
    sub_counties_list = [{'sub_county': 'Sub county'}]
    sub_counties_list += [{'sub_county': sub_county.sub_cnty} for sub_county in sub_counties]
    return JsonResponse(sub_counties_list, safe=False)

def load_locations(request):
    sub_county = request.GET.get('sub_county')
    locations = AdminBoundaries.objects.filter(sub_cnty=sub_county).order_by('location').distinct('location')
    locations_list = [{'location': 'Location'}]
    locations_list += [{'location': location.location} for location in locations]
    return JsonResponse(locations_list, safe=False)

def load_sub_locations(request):
    location = request.GET.get('location')
    sub_locations = AdminBoundaries.objects.filter(location=location).order_by('sub_locat').distinct('sub_locat')
    sub_locations_list  = [{'sub_location': 'Sub location'}]
    sub_locations_list += [{'sub_location': sub_location.sub_locat} for sub_location in sub_locations]
    return JsonResponse(sub_locations_list, safe=False)

# Geocoding
def save_user_data(first_name, last_name,phone_number, county, sub_county, location, sub_location):
    geolocator = Nominatim(user_agent="EarlyWarningSystem")
    location_data = geolocator.geocode(location)

    if location_data:
        latitude = location_data.latitude
        longitude = location_data.longitude


        userdata.objects.create(
            first_name = first_name,
            last_name=last_name,
            phone_number=phone_number,
            location=location,
            county=county,
            sub_county=sub_county,
            sub_location=sub_location,
            latitude=latitude,
            longitude=longitude
        )
    else:
        # Handle the case where location_data is None (geocoding failed)
        pass




def send_sms(phone_number):
    account_sid = settings.account_sid
    auth_token = settings.auth_token
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        messaging_service_sid='MG5d340a14f88312ffa03d5865521f7347',
        body='Flood Watch in effect for Budalangi Sub_county for the next 2 weeks. Heavy rainfall expected.Stay informed and be prepared to move to higher grounds if flooding occurs.',
        to=phone_number
        )
    print(message.sid)
    
    
    


def is_within_flood_prone_area(latitude, longitude):
    # Define flood-prone area boundaries
    min_latitude = -0.11
    max_latitude = 0.37
    min_longitude = 33.57
    max_longitude = 34.14
    if latitude is not None and longitude is not None:
        if min_latitude <= latitude <= max_latitude and min_longitude <= longitude <= max_longitude:
            return True

    return False



def success_page(request):
    return render(request, 'success_page.html')




def user_data_form(request):
    phone_numbers = userdata.objects.values_list('phone_number', flat=True)
    if request.method == 'POST':
        form = UserDataForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            with transaction.atomic():
                # Extract cleaned data from the form
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                phone_number = form.cleaned_data['phone_number']
                county = form.cleaned_data['county']
                sub_county = form.cleaned_data['sub_county']
                location = form.cleaned_data['location']
                sub_location = form.cleaned_data['sub_location']
                save_user_data(first_name, last_name,phone_number, county, sub_county, location, sub_location)
            for phone_number in phone_numbers:
                send_sms(phone_number)    
                # Additional operations, if needed

            return redirect('success_page')
        
    else:
        form = UserDataForm()

    return render(request, 'user_data_form.html', {'form': form})

def process_water_levels(filename):
    # Load the Excel sheet
    workbook = openpyxl.load_workbook(filename)
    sheet = workbook.active

    # Iterate through each row in the sheet
    for row in sheet.iter_rows(min_row=2, values_only=True):
        latitude = row[0]
        longitude = row[1]
        water_level = row[2]

        if water_level > 3:
            # Retrieve user data from PostgreSQL database
            user_data = userdata.objects.all()
            for user in user_data:
                user_latitude = user.latitude
                user_longitude = user.longitude
                user_phone_number = user.phone_number

                if is_within_flood_prone_area(user_latitude, user_longitude):
                    message = f"Warning: You are in a flood-prone area. Take necessary precautions!"
                    send_sms(user_phone_number, message)

    workbook.close()




