from django import forms
from .models import userdata, AdminBoundaries

class UserDataForm(forms.ModelForm):
    county = forms.ModelChoiceField(
        queryset=AdminBoundaries.objects.order_by('county').distinct('county'),
        to_field_name="county"
    )
    sub_county = forms.ModelChoiceField(
        queryset=AdminBoundaries.objects.none(),
        to_field_name="sub_cnty"
    )
    location = forms.ModelChoiceField(
        queryset=AdminBoundaries.objects.none(),
        to_field_name="location"
    )
    sub_location = forms.ModelChoiceField(
        queryset=AdminBoundaries.objects.none(),
        to_field_name="sub_locat"
    )

    class Meta:
        model = userdata
        fields = ['first_name', 'last_name', 'phone_number', "county", "sub_county", "location", "sub_location"]

    def __init__(self, *args, **kwargs):
        super(UserDataForm, self).__init__(*args, **kwargs)

        if 'county' in self.data:
            try:
                county_id = self.data.get('county')
                self.fields['sub_county'].queryset = AdminBoundaries.objects.filter(county=county_id).order_by('sub_cnty').distinct('sub_cnty')
            except (ValueError, TypeError):
                self.fields['sub_county'].queryset = AdminBoundaries.objects.none()
        elif self.instance.pk and self.instance.county:
            self.fields['sub_county'].queryset = AdminBoundaries.objects.filter(county=self.instance.county).order_by('sub_cnty').distinct('sub_cnty')

        if 'sub_county' in self.data:
            try:
                sub_county_id = self.data.get('sub_county')
                self.fields['location'].queryset = AdminBoundaries.objects.filter(sub_cnty=sub_county_id).order_by('location').distinct('location')
            except (ValueError, TypeError):
                self.fields['location'].queryset = AdminBoundaries.objects.none()
        elif self.instance.pk and self.instance.sub_county:
            self.fields['location'].queryset = AdminBoundaries.objects.filter(sub_cnty=self.instance.sub_county).order_by('location').distinct('location')

        if 'location' in self.data:
            try:
                location_id = self.data.get('location')
                self.fields['sub_location'].queryset = AdminBoundaries.objects.filter(location=location_id).order_by('sub_locat').distinct('sub_locat')
            except (ValueError, TypeError):
                self.fields['sub_location'].queryset = AdminBoundaries.objects.none()
        elif self.instance.pk and self.instance.location:
            self.fields['sub_location'].queryset = AdminBoundaries.objects.filter(location=self.instance.location).order_by('sub_locat').distinct('sub_locat')