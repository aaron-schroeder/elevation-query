# Define avg Earth radius in meters according to International
# Union of Geodesy and Geophysics.
EARTH_RADIUS_METERS = 6371E3


def great_circle(lon1, lat1, lon2, lat2):
  from math import sin, cos, asin, radians, sqrt
  lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
  dlon = lon2 - lon1
  dlat = lat2 - lat1

  # Since I will be in the same ~12 mi area the whole time, certain
  # of these terms might be negligible and the calculation can
  # speed up. But which terms, based on my specific area??
  a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2

  c = 2 * asin(min(1, sqrt(a)))
  d = EARTH_RADIUS_METERS * c

  return d


def flat_earth(lon1, lat1, lon2, lat2):
  """Just using Cartesian coordinates."""
  from math import sin, cos, asin, radians
  lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

  # Could simplify this by defining a single cos for the entire rt.
  dx = EARTH_RADIUS_METERS * (lon2 - lon1) * cos((lat1 + lat2) / 2)

  dy = EARTH_RADIUS_METERS * (lat2 - lat1) 

  return (dx ** 2 + dy ** 2) ** 0.5


def great_circle_geopy(lon1, lat1, lon2, lat2):
  import geopy

  return geopy.distance.great_circle((lat1, lon1), (lat2, lon2))
