import os

import pandas as pd
import geopandas as gpd
# TODO: Load coordinates into geospatial structures

data_dir = os.path.join(os.path.dirname(__file__), 'data')


def parse_coordinates(ports_df):
    """
    Convert degrees, minutes and hemisphere data
    into standardised coordinate format
    """
    raise NotImplementedError


def load_all_ports():
    ports = pd.read_csv(os.path.join(data_dir, 'file.csv'))
    coord_cols = ['latitudeDegrees', 'latitudeMinutes', 'latitudeHemisphere',
                  'longitudeDegrees', 'longitudeMinutes',
                  'longitudeHemisphere']
    ports = ports[['portNumber', 'portName'] + coord_cols]
    ports = parse_coordinates(ports)
