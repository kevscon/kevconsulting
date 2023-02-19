import fractions
import numpy as np

def format_num(num, decimal_len=3):
    try:
        num_str = str(num)
        num_float = float(sum(fractions.Fraction(s) for s in num_str.split()))
        num_formatted = ("{:." + str(decimal_len) + "f}").format(num_float).rstrip('0').rstrip('.')
        return num_formatted
    except:
        return num

class ShapeProperties:

    def __init__(self, shape_df):
        self.shape_df = shape_df

    def select_shape_data(self, shape_label, shape_section=None, shape_type=None, edition=None):
        self.shape_section = shape_section
        self.shape_label = shape_label
        self.shape_type = shape_type
        self.edition = edition
        if edition == None:
            self.selected_rows = self.shape_df[self.shape_df['EDI_Std_Nomenclature'] == shape_label]
        else:
            self.selected_rows = self.shape_df[(self.shape_df['Edition'] == edition) & (self.shape_df['Designation'] == shape_label)]

    def format_shape_data(self, properties_to_output):
        if self.edition == None:
            selected_columns = self.selected_rows[properties_to_output]
        else:
            properties_to_output[0] = 'Designation'
            properties_to_output.insert(0, 'Edition')
            selected_columns = self.selected_rows[properties_to_output]
        selected_columns.replace(to_replace='0', value='–', inplace=True)
        filtered_columns = selected_columns.replace(to_replace='–', value=np.nan).dropna(axis=1, how='all').fillna('–')
        self.headers = filtered_columns.columns
        self.output_data = filtered_columns.applymap(format_num)

    def create_output_dict(self, table_header_dict):
        output_dict = {}
        if self.edition == None:
            output_dict['shape_section'] = self.shape_section
        else:
            output_dict['shape_type'] = self.shape_type
        output_dict['selected_properties'] = self.output_data.values
        output_dict['property_headers'] = [table_header_dict[header][1] for header in self.headers]
        output_dict['unit_headers'] = [table_header_dict[header][2] for header in self.headers]
        return output_dict

    def export_properties(self, output_filepath):
        if self.edition == None:
            output_df = self.shape_df[self.shape_df['EDI_Std_Nomenclature'] == self.shape_label]
        else:
            output_df = self.shape_df[(self.shape_df['Edition'] == self.edition) & (self.shape_df['Designation'] == self.shape_label)]
        output_df.to_excel(output_filepath, index=False)
