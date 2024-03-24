from __future__ import unicode_literals
from django.contrib.gis.db import models
from django.contrib.auth.models import Group

# Create your models here.


class AdminBoundaries(models.Model):
    iso = models.CharField(max_length=3, blank=False, null=True)
    country = models.CharField(max_length=75,blank=False, null=True)
    county = models.CharField(max_length=75,blank=False, null=True)
    sub_cnty = models.CharField(max_length=75,blank=False, null=True)
    location = models.CharField(max_length=100,blank=False, null=True)
    sub_locat = models.CharField(max_length=75,blank=False, null=True)
    country_id = models.BigIntegerField(default=0)
    county_id = models.BigIntegerField(default=0)
    sb_cnt_id = models.BigIntegerField(default=0)
    locat_id = models.BigIntegerField(default=0)
    sb_loca_id = models.BigIntegerField(default=0)
    geom = models.MultiPolygonField(srid=4326, null=True)
   
    def __str__(self):
        if  self.county:
            return self.county

        elif self.sub_cnty:
            return self.sub_cnty

        elif self.location:
            return self.location
        elif self.sub_locat:
            return self.sub_locat
        else:
            return "Unnamed"
    class Meta:
        ordering = ["county", "sub_cnty", "location", "sub_locat"]


class UserData(models.Model):
    id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=False, null=True)
    opt_in_alerts = models.BooleanField(default=False)
    country = models.ForeignKey('AdminBoundaries', on_delete=models.SET_NULL, null=True, blank=True, related_name='user_data_country')
    county = models.ForeignKey('AdminBoundaries', on_delete=models.SET_NULL, null=True, blank=True, related_name='user_data_county')
    sub_county = models.ForeignKey('AdminBoundaries', on_delete=models.SET_NULL, null=True, blank=True, related_name='user_data_sub_county')
    location = models.ForeignKey('AdminBoundaries', on_delete=models.SET_NULL, null=True, blank=True, related_name='user_data_location')
    sub_location = models.ForeignKey('AdminBoundaries', on_delete=models.SET_NULL, null=True, blank=True, related_name='user_data_sub_location')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
   
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.phone_number})"

    groups = models.ManyToManyField(Group, related_name='ews_user_set')




  