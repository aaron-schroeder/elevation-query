"""Functions to get elevation data of various sources from GPS coordinates."""

import requests


def national_map_epqs(latlon_coords):
  """USGS Elevation Point Query Service - 1/3 arcsecond data.
  
  Args:
    latlon_coords (list of tuples): series of (lat, lon) coords.

  Returns:
    list of floats: Elevation values sampled from the NED elevation
      point query service (EPQS). As of this writing, that's their
      1/3 arc-second data.
  """

  # Force ipv4 for national map requests (times out w/ ipv6)
  import socket
  import requests.packages.urllib3.util.connection as urllib3_cn
  def allowed_gai_family():
    family = socket.AF_INET    # force IPv4
    return family
  urllib3_cn.allowed_gai_family = allowed_gai_family

  url = r'https://nationalmap.gov/epqs/pqs.php?'

  from concurrent import futures
  with futures.ThreadPoolExecutor(max_workers=None) as executor:
    futures = [
      executor.submit(
        lambda: requests.get(
          url, 
          params={'output': 'json', 'units': 'Meters', 'x': lon, 'y': lat})
        )
        # This way is a bit slower:
        #lambda: requests.post(url, data={'output': 'json', 'units': 'Meter', 'x': x, 'y': y}))
      for (lat, lon) in latlon_coords
    ]

  elevation_array = [
    f.result().json()['USGS_Elevation_Point_Query_Service']['Elevation_Query']['Elevation']
    for f in futures
  ]

  return elevation_array


def national_map_1m(latlon_coords, elevation_fname):
  """USGS National Map - 1m data (lidar).
  
  Args:
    latlon_coords (list of tuples): series of (lat, lon) coords.

  Returns:
    list of floats: Elevation values sampled from the NED 1m dataset.
      Lidar data! The highest resolution data I know of.

  """
  # Rasterio 1.2 works with Python versions 3.6 through 3.9,
  # Numpy versions 1.15 and newer, and GDAL versions 2.3 through 3.2.

  import rasterio
  from pyproj import Transformer

  with rasterio.open(elevation_fname) as src:
    crs_from = "epsg:4326"  # regular ol lat/lon
    
    # the specific UTM coord system (Zone 13N for me)
    # https://georepository.com/crs_26913/NAD83-UTM-zone-13N.html
    crs_to = src.crs
    transformer = Transformer.from_crs(crs_from, crs_to)

    utm_coords_generator = transformer.itransform(latlon_coords)

    # val is an array of values, 1 element per band. 
    # src is a single band raster so we only need val[0].
    elev_array = list(val[0] for val in src.sample(utm_coords_generator))

  return elev_array


def open_elevation(latlon_coords):
  """Elevation values from the open-elevation API.
  
  https://github.com/Jorl17/open-elevation/blob/master/docs/api.md

  Super slow. And times out (504) - need to catch that.
  Known issue: https://github.com/Jorl17/open-elevation/issues/29

  Args:
    latlon_coords (list of tuples): series of (lat, lon) coords.

  Returns:
    list of floats: Elevation values returned from open-elevation's
      REST API.

  """

  url = 'https://api.open-elevation.com/api/v1/lookup'

  location_payload = {
    'locations': [
      {'latitude': lat, 'longitude': lon} for lat, lon in latlon_coords
    ]
  }

  resp = requests.post(url, json=location_payload)

  elevation_array = [
      result['elevation'] for result in resp.json()['results']
  ]

  return elevation_array


def google(latlon_coords, user_gmaps_key, units='meters'):
  """Queries google maps' Elevation API at each point.
  
  Args:
    latlon_coords (list of tuples): series of (lat, lon) coords.
    units (str): desired output units, 'meters', or 'feet'. 
      Default 'meters'.

  Returns:
    list of floats: Elevation values from Google Maps Elevation API.
      Taken from a variety of sources, mainly the SRTM.

  """
  import math

  import googlemaps
  import numpy as np

  gmaps = googlemaps.Client(key=user_gmaps_key)
  
  latlons = np.array(latlon_coords)

  # Google maps elevation api allows 500 elevation values
  # per request. Break latlon coordinates into 500-piece chunks
  # and pass to the api, then assemble returned elevations into one
  # consolidated list, and add to dataframe as a new column.
  unit_factor = 5280.0 / 1609 if units.lower() == 'feet' else 1.0
  elevs = []

  num_sections = math.ceil(len(latlons) / 500)
  for chunk in np.array_split(latlons, num_sections):

    # Format coordinates for google maps api request
    locations = [(float(latlon[0]), float(latlon[1])) for latlon in chunk]
    response = gmaps.elevation(locations)

    elevs.extend([round(elevobj['elevation'] * unit_factor, 1) 
        for elevobj in response])
  
  return elevs