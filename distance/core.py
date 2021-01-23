# -*- coding: utf-8 -*-
import math

import numpy as np
import pandas as pd

from . import helpers


EARTH_RADIUS_METERS = helpers.EARTH_RADIUS_METERS


def spherical_earth_plane_displacement(lat_series, lon_series):
  """Example function with types documented in the docstring.

  An example `PEP 484`_ type annotations are supported. If attribute,
  parameter, and return types are annotated according to `PEP 484`_, they 
  do not need to be included in the docstring:
  
  Parameters
  ----------
  lat_series : pandas.Series
      Latitude values.
  lon_series : pandas.Series
      Longitude values.

  Returns
  -------
  pandas.Series
      Point-to-point displacements in meters.
  
  Notes
  -----

  Assumptions:
      * Earth is a perfect sphere, with radius = EARTH_RADIUS_METERS.
      * The point-to-point distances are sufficiently short (so that
        latitude distortion and curvature have limited effects).
      * Both lat_series and lon_series units are degrees.
  
  `Numpy docstring ref`_

  `Numpy docstring example`_

  `Google docstring example`_

  `Sphinx todos`_  

  Todo: 
      * Update these assumpts!
      * Figure out `Sphinx todos`_!


  .. _PEP 484:
      https://www.python.org/dev/peps/pep-0484/
      
  .. _Numpy docstring ref:
      https://numpydoc.readthedocs.io/en/latest/format.html

  .. _Numpy docstring example:
      https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_numpy.html

  .. _Google docstring example:
      https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

  .. _Sphinx todos:
      https://www.sphinx-doc.org/en/master/usage/extensions/todo.html

  """
  # Convert to radians.
  lat_series = lat_series * math.pi / 180
  lon_series = lon_series * math.pi / 180

  # Project the spherical coordinates onto a plane.
  dx = EARTH_RADIUS_METERS * np.cos(lat_series) * lon_series.diff()
  dy = EARTH_RADIUS_METERS * lat_series.diff()

  # Calculate point-to-point displacements on the plane.
  ds = (dx ** 2 + dy ** 2) ** 0.5

  # Remove the NaN value in the first position.
  return ds.fillna(0.)


def from_disp(disp_series):
  return disp_series.cumsum()


def from_dist(dist_series):
  return dist_series.diff()


def from_speed(speed_series, time_series):
  time_series = time_series or pd.Series([i for i in range(len(speed_series))])

  return speed_series * time_series