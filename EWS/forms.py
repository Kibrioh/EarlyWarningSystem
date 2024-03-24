from django import forms
from .models import UserData, AdminBoundaries

class UserDataForm(forms.ModelForm):
    class Meta:
        model = UserData
        fields = ['first_name', 'last_name', 'phone_number', 'opt_in_alerts', 'county', 'sub_county', 'location', 'sub_location']

    def __init__(self, *args, **kwargs):
        super(UserDataForm, self).__init__(*args, **kwargs)


        # Set id attribute for each form field
        self.fields['first_name'].widget.attrs['id'] = 'id_first_name'
        self.fields['last_name'].widget.attrs['id'] = 'id_last_name'
        self.fields['phone_number'].widget.attrs['id'] = 'id_phone_number'
        self.fields['opt_in_alerts'].widget.attrs['id'] = 'id_opt_in_alerts'
        self.fields['county'].widget.attrs['id'] = 'id_county'
        self.fields['sub_county'].widget.attrs['id'] = 'id_sub_county'
        self.fields['location'].widget.attrs['id'] = 'id_location'
        self.fields['sub_location'].widget.attrs['id'] = 'id_sub_location'

         # Populate county dropdown
        counties = AdminBoundaries.objects.order_by('county').distinct('county').values_list('county', flat=True)
        self.fields['county'].choices = [(county, county) for county in counties]


      # Populate sub_county dropdown based on selected county
        if 'county' in self.data:
            county_name = self.data.get('county')
    # Filter AdminBoundaries objects by county name
            sub_counties = AdminBoundaries.objects.filter(county=county_name).order_by('sub_cnty').distinct('sub_cnty').values_list('sub_cnty', flat=True)
            self.fields['sub_county'].choices = [(sub_county, sub_county) for sub_county in sub_counties]
        elif self.instance and self.instance.county:
            county_name = self.instance.county
    # Filter AdminBoundaries objects by county name from instance
            sub_counties = AdminBoundaries.objects.filter(county=county_name).order_by('sub_cnty').distinct('sub_cnty').values_list('sub_cnty', flat=True)
            self.fields['sub_county'].choices = [(sub_county, sub_county) for sub_county in sub_counties]
        else:
    # No county selected, so set choices to empty list
            self.fields['sub_county'].choices = []

        # Populate location dropdown based on selected sub_county
        if 'sub_county' in self.data:
            sub_county_name = self.data.get('sub_county')
            self.fields['location'].queryset = AdminBoundaries.objects.filter(sub_cnty=sub_county_name).values_list('location', flat=True).distinct()
        elif self.instance.sub_county:
            self.fields['location'].queryset = AdminBoundaries.objects.filter(sub_cnty=self.instance.sub_county).values_list('location', flat=True).distinct()

        # Populate sub_location dropdown based on selected location
        if 'location' in self.data:
            location_name = self.data.get('location')
            self.fields['sub_location'].queryset = AdminBoundaries.objects.filter(location=location_name).values_list('sub_locat', flat=True).distinct()
        elif self.instance.location:
            self.fields['sub_location'].queryset = AdminBoundaries.objects.filter(location=self.instance.location).values_list('sub_locat', flat=True).distinct()