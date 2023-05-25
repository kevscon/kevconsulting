import os
import pandas as pd
from flask import request

directory = os.getcwd() + '/app/app/nbi_search/data/'
output_filepath = directory + 'nbi_output.xlsx'
year = '2022'

state_fips_df = pd.read_csv(directory + 'fips/state_fips.txt', sep="|", dtype=str)
county_fips_df = pd.read_csv(directory + 'fips/county_fips.txt', sep=",", dtype=str, header=None)
place_fips_df = pd.read_csv(directory + 'fips/place_fips.txt', sep="|", dtype=str, encoding = "ISO-8859-1")
from app.app.nbi_search.classes import FIPSData


def get_states():
    state_options = [(None, '--select state--')]
    state_options += list(zip(state_fips_df['STUSAB'], state_fips_df['STATE_NAME']))
    remove_list = [('AS', 'American Samoa'), ('MP', 'Northern Mariana Islands'), ('UM', 'U.S. Minor Outlying Islands')]
    for item in remove_list:
        state_options.remove(item)
    return state_options


def filter_counties(state_postal):
    from app.app.nbi_search.classes import FIPSData
    fips_class = FIPSData(state_fips_df, county_fips_df, place_fips_df)
    fips_class.get_state_fips(state_postal)
    county_names = fips_class.get_counties()
    return county_names


def filter_bridges():
    state_postal = request.form['state_postal']
    county_name = request.form['county_name']

    from app.app.nbi_search.classes import FIPSData
    fips_class = FIPSData(state_fips_df, county_fips_df, place_fips_df)
    fips_class.get_state_fips(state_postal)

    from app.app.nbi_search.classes import NBIBridgeSearch
    nbi_class = NBIBridgeSearch(directory, year, state_postal)
    county_fips = fips_class.get_county_fips(county_name)
    county_bridges_df = nbi_class.get_county_bridges(county_fips)
    county_bridges_df['FACILITY_CARRIED_007'] = county_bridges_df['FACILITY_CARRIED_007']\
        .apply(lambda x: str(x).replace("'", ''))
    county_bridges_df['FEATURES_DESC_006A'] = county_bridges_df['FEATURES_DESC_006A']\
        .apply(lambda x: str(x).replace("'", ''))

    bridge_list = county_bridges_df.to_dict('records')
    return bridge_list


def return_bridge_properties(state_postal, structure_number):

    from app.app.nbi_search.classes import NBIBridgeSearch
    nbi_class = NBIBridgeSearch(directory, year, state_postal)
    bridge_data_df = nbi_class.get_bridge_data(structure_number)
    nbi_class.export_data(output_filepath)
    bridge_data = bridge_data_df.copy().squeeze()

    def format_description(description):
        return description.replace("'", '')

    def format_latitude(latitude_dms):
        seconds = float(latitude_dms[-4:])/100
        minutes = int(latitude_dms[2:4])
        degrees = int(latitude_dms[0:2])
        return degrees + minutes/60 + seconds/3600

    def format_longitude(longitude_dms):
        seconds = float(longitude_dms[-4:])/100
        minutes = int(longitude_dms[3:5])
        degrees = int(longitude_dms[0:3])
        return -1*(degrees + minutes/60 + seconds/3600)

    def format_dimension(meter_dimension):
        meter_to_foot_factor = 3.2808398950131235
        foot_dimension = float(meter_dimension) * meter_to_foot_factor
        return '{0:.2f}'.format(foot_dimension)

    material_dict = {
        '1': 'Concrete',
        '2': 'Concrete continuous',
        '3': 'Steel',
        '4': 'Steel continuous',
        '5': 'Prestressed concrete',
        '6': 'Prestressed concrete continuous',
        '7': 'Wood or Timber',
        '8': 'Masonry',
        '9': 'Aluminum, Wrought Iron, or Cast Iron',
        '0': 'Other'
    }

    bridge_data['FACILITY_CARRIED_007'] = format_description(bridge_data['FACILITY_CARRIED_007'])
    bridge_data['FEATURES_DESC_006A'] = format_description(bridge_data['FEATURES_DESC_006A'])

    fips_class = FIPSData(state_fips_df, county_fips_df, place_fips_df)
    bridge_data['STATE_CODE_001'] = fips_class.get_state_name(bridge_data['STATE_CODE_001'])
    bridge_data['COUNTY_CODE_003'] = fips_class.get_county_name(bridge_data['COUNTY_CODE_003'])
    try:
        bridge_data['PLACE_CODE_004'] = fips_class.get_place_name(bridge_data['PLACE_CODE_004'])
    except:
        bridge_data['PLACE_CODE_004'] = 'N/A'

    bridge_data['LAT_016'] = format_latitude(bridge_data['LAT_016'])
    bridge_data['LONG_017'] = format_longitude(bridge_data['LONG_017'])

    bridge_data['STRUCTURE_LEN_MT_049'] = format_dimension(bridge_data['STRUCTURE_LEN_MT_049'])

    bridge_data['STRUCTURE_KIND_043A'] = material_dict[bridge_data['STRUCTURE_KIND_043A']]

    return bridge_data
