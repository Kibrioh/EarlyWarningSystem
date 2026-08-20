import os
from django.contrib.gis.utils import LayerMapping
from .models import AdminBoundaries

# Auto-generated `LayerMapping` dictionary for AdminBoundaries model
adminboundaries_mapping = {
    'iso': 'ISO',
    'country': 'Country',
    'county': 'County',
    'sub_cnty': 'Sub_CNTY',
    'location': 'Location',
    'sub_locat': 'Sub_LOCAT',
    'country_id': 'Country_ID',
    'county_id': 'County_ID',
    'sb_cnt_id': 'Sb_CNT_ID',
    'locat_id': 'Locat_ID',
    'sb_loca_id': 'Sb_LOCA_ID',
    'geom': 'MULTIPOLYGON',
}

AdminBoundaries_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Data', 'Data.shp'),)
def run(verbose=False):
    lm = LayerMapping(AdminBoundaries, AdminBoundaries_shp, adminboundaries_mapping, transform= False, 
    encoding='iso-8859-1')
    lm.save(strict=True,verbose=verbose)