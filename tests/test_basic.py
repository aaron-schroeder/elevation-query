# -*- coding: utf-8 -*-

import query

import unittest


class TestAlgorithms(unittest.TestCase):

  def setUp(self):
    # Generate some BS coordinates that are in the range of all
    # elevation services.
    self.latlons = [
      (40.03488860164351, -105.27230724626),
      (40.03498860164351, -105.27230724626),
      (40.03508860164351, -105.27230724626),
      (40.03518860164351, -105.27230724626),
      (40.03528860164351, -105.27230724626),
      (40.03538860164351, -105.27230724626),
      (40.03548860164351, -105.27230724626),
      (40.03558860164351, -105.27230724626),
      (40.03568860164351, -105.27230724626),
      (40.03578860164351, -105.27230724626)
    ]

  def test_epqs(self):
    """Functional test for National Map EPQS."""
    elevs = query.national_map_epqs(self.latlons)
    
    # print('epqs')
    # print(elevs)

    self.assertIsInstance(elevs, list)

  @unittest.skip(
   'This test only works on my local machine because it makes use of '
   'a file over here. WIP.'
  )
  def test_1m(self):
    """Functional test for National Map 1m file."""
    
    # I am not including this dataset for now - it is huge.
    # Maybe at some point.
    elevation_fname = 'data/all.tif'
    
    elevs = query.national_map_1m(self.latlons, elevation_fname)
    
    # print('1m')
    # print(elevs)

    self.assertIsInstance(elevs, list)

  @unittest.skip('open-elevation works, but it is sloooow.')
  def test_open_elevation(self):
    elevs = query.open_elevation(self.latlons)
    
    # print('open_elevation')
    # print(elevs)
    
    self.assertIsInstance(elevs, list)

  def test_google_maps(self):
    # Note: Running this test requires a user-maintained `config.py`
    # file containing their gmaps key as a string.
    from config import user_gmaps_key

    # Generate enough latlons that the request needs to be broken
    # up into chunks.
    latlons = [[40.0, -105.0]] * 10000

    elevs = query.google(latlons, user_gmaps_key)

    # print('google maps')
    # print(elevs)

    self.assertIsInstance(elevs, list)


if __name__ == '__main__':
  unittest.main()