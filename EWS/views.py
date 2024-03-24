from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from EWS.forms import UserDataForm
from django.http import HttpResponse
from geopy.geocoders import Nominatim
from twilio.rest import Client
from EWS.models import UserData, AdminBoundaries
from django.conf import settings
import openpyxl
# view functions

def load_counties(request):
    distinct_counties = AdminBoundaries.objects.values_list('county').distinct('county')
    counties_list = [{'county_name': county} for county in distinct_counties]
    return JsonResponse(counties_list, safe=False)

def load_sub_counties(request):
    county_name = request.GET.get('county_name')
    sub_counties = AdminBoundaries.objects.filter(county=county_name).order_by('sub_cnty').values_list('sub_cnty', flat=True).distinct()
    sub_counties_list = [{'sub_county_name': sub_county} for sub_county in sub_counties]
    return JsonResponse(sub_counties_list, safe=False)

def load_locations(request):
    sub_county_name = request.GET.get('sub_county_name')
    locations = AdminBoundaries.objects.filter(sub_cnty=sub_county_name).order_by('location').values_list('location', flat=True).distinct()
    locations_list = [{'location_name': location} for location in locations]
    return JsonResponse(locations_list, safe=False)

def load_sub_locations(request):
    location_name = request.GET.get('location_name')
    sub_locations = AdminBoundaries.objects.filter(location=location_name).order_by('sub_locat').values_list('sub_locat', flat=True).distinct()
    sub_locations_list = [{'sub_location_name': sub_location} for sub_location in sub_locations]
    return JsonResponse(sub_locations_list, safe=False)


# Geocoding
def save_user_data(first_name, last_name,phone_number,sub_location):
    geolocator = Nominatim(user_agent="EarlyWarningSystem")
    location_data = geolocator.geocode(sub_location)

    if location_data:
        latitude = location_data.latitude
        longitude = location_data.longitude

        # Get or create the AdminBoundaries instance based on the user's location
        admin_boundaries_instance, created = AdminBoundaries.objects.get_or_create(
            sub_location=sub_location  
        )

        UserData.objects.create(
            first_name = first_name,
            last_name=last_name,
            phone_number=phone_number,
            sub_location=admin_boundaries_instance,
            latitude=latitude,
            longitude=longitude
        )
    else:
        # Handle the case where location_data is None (geocoding failed)
        pass




def send_sms(phone_number, message):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=message,
        from_=settings.TWILIO_PHONE_NUMBER,
        to=phone_number,
    )
    print(message.sid)
    
    
    


def is_within_flood_prone_area(latitude, longitude):
    # Define flood-prone area boundaries
    min_latitude = -0.11
    max_latitude = 0.04
    min_longitude = 33.57
    max_longitude = 34.14
    if latitude is not None and longitude is not None:
        if min_latitude <= latitude <= max_latitude and min_longitude <= longitude <= max_longitude:
            return True

    return False





def user_data_form(request):
    if request.method == 'POST':
        form = UserDataForm(request.POST)
        if form.is_valid():
            print(request.POST)
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            phone_number = form.cleaned_data.get('phone_number')
            sub_location = form.cleaned_data.get('sub_location')

            print("First Name:", first_name)
            print("Last Name:", last_name)
            print("Phone Number:", phone_number)
            print("Sub Location:", sub_location)

            save_user_data(first_name, last_name, phone_number, sub_location)
            filename = 'C:/Users/User/Downloads/Brian/5.1/Project/water_levels.xlsx'
            process_water_levels(filename)
            return HttpResponse("Early warning sent successfully.")
        return redirect('success_page')  # Redirect to a success page
    else:
        form = UserDataForm()

    return render(request, 'user_data_form.html', {'form': form})

def success_page(request):
    return render(request, 'success_page.html')




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
            user_data = UserData.objects.all()
            for user in user_data:
                user_latitude = user.latitude
                user_longitude = user.longitude
                user_phone_number = user.phone_number

                if is_within_flood_prone_area(user_latitude, user_longitude):
                    message = f"Warning: You are in a flood-prone area. Take necessary precautions!"
                    send_sms(user_phone_number, message)

    workbook.close()




