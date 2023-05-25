import pandas as pd

# verify dataframe column names
class FIPSData:

    def __init__(self, state_fips_df, county_fips_df, place_fips_df):
        self.state_fips_df = state_fips_df
        self.county_fips_df = county_fips_df
        self.place_fips_df = place_fips_df

    def get_state_name(self, state_id):
        if state_id.isdigit():
            self.state_fips = state_id
            state_name = self.state_fips_df['STATE_NAME'][self.state_fips_df['STATE'] == state_id].values
        else:
            state_fips = self.state_fips_df['STATE'][self.state_fips_df['STUSAB'] == state_id].values
            self.state_fips = state_fips[0]
            state_name = self.state_fips_df['STATE_NAME'][self.state_fips_df['STUSAB'] == state_id].values
        return state_name[0]

    def get_state_postal(self, state_id):
        try:
            state_postal = self.state_fips_df['STUSAB'][self.state_fips_df['STATE'] == state_id].values
            self.state_postal = state_postal[0]
            self.state_fips = state_id
        except:
            state_postal = self.state_fips_df['STUSAB'][self.state_fips_df['STATE_NAME'] == state_id].values
            self.state_postal = state_postal[0]
            state_fips = self.state_fips_df['STATE'][self.state_fips_df['STATE_NAME'] == state_id].values
            self.state_fips = state_fips[0]
        return self.state_postal

    def get_state_fips(self, state_id):
        try:
            state_fips = self.state_fips_df['STATE'][self.state_fips_df['STUSAB'] == state_id].values
            self.state_fips = state_fips[0]
        except:
            state_fips = self.state_fips_df['STATE'][self.state_fips_df['STATE_NAME'] == state_id].values
            self.state_fips = state_fips[0]
        return self.state_fips

    def get_county_name(self, county_fips, state_fips=''):
        if state_fips == '':
            state_fips = self.state_fips
        county_name = self.county_fips_df[3][(self.county_fips_df[1] == state_fips)
                                        & (self.county_fips_df[2] == county_fips)].values
        self.county_name = list(county_name)[0]
        return self.county_name

    def get_county_fips(self, county_name, state_fips=''):
        if state_fips == '':
            state_fips = self.state_fips
        self.county_name = county_name
        county_fips = self.county_fips_df[2][(self.county_fips_df[1] == state_fips)
                                        & (self.county_fips_df[3] == county_name)].values
        self.county_fips = list(county_fips)[0]
        return self.county_fips

    def get_place_name(self, place_fips, county_name='', state_fips=''):
        if state_fips == '':
            state_fips = self.state_fips
        if county_name == '':
            county_name = self.county_name
        place_name = self.place_fips_df['PLACENAME'][(self.place_fips_df['STATEFP'] == state_fips)
                                 & (self.place_fips_df['COUNTY'] == county_name)
                                 & (self.place_fips_df['PLACEFP'] == place_fips)].values
        return place_name[0]

    def get_place_fips(self, place_name, county_name='', state_fips=''):
        if state_fips == '':
            state_fips = self.state_fips
        if county_name == '':
            county_name = self.county_name
        place_fips = self.place_fips_df['PLACEFP'][(self.place_fips_df['STATEFP'] == state_fips)
                                 & (self.place_fips_df['COUNTY'] == county_name)
                                 & (self.place_fips_df['PLACENAME'] == place_name)].values
        return place_fips[0]

    def get_counties(self, state_fips=''):
        if state_fips == '':
            state_fips = self.state_fips
        county_names = self.county_fips_df[3][self.county_fips_df[1] == state_fips].values
        return list(county_names)

    def get_places(self, county_name='', state_fips=''):
        if state_fips == '':
            state_fips = self.state_fips
        if county_name == '':
            county_name = self.county_name
        place_names = self.place_fips_df['PLACENAME'][(self.place_fips_df['STATEFP'] == state_fips)
                                                 & (place_fips_df['COUNTY'] == county_name)]
        return list(place_names)


def create_nbi_filepath(directory, year, state_postal):
    return directory + year + 'del/' + state_postal + year[-2:] + '.txt'

# verify dataframe column names
class NBIBridgeSearch:

    def __init__(self, directory, year, state_postal):
        filepath = create_nbi_filepath(directory, year, state_postal)
        self.state_df = pd.read_csv(filepath, sep=",", dtype=object)
        self.state_df['STRUCTURE_NUMBER_008'] = self.state_df['STRUCTURE_NUMBER_008']\
            .apply(lambda x: str(x).strip())

    def get_county_bridges(self, county_fips):
        self.county_df = self.state_df[self.state_df['COUNTY_CODE_003'] == county_fips]
        return self.county_df

    def get_place_bridges(self, place_fips):
        self.place_df = self.county_df[self.county_df['PLACE_CODE_004'] == place_fips]
        return self.place_df

    def get_bridge_data(self, structure_number):
        self.bridge_data = self.state_df[self.state_df['STRUCTURE_NUMBER_008'] == structure_number]
        return self.bridge_data

    def export_data(self, output_filepath):
        output_df = self.bridge_data
        output_df.to_excel(output_filepath, index=False)
