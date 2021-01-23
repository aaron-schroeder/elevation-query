# -*- coding: utf-8 -*-

import distance

import unittest

import pandas as pd
import numpy as np

#import heartandsole.algorithms as algs


class TestAlgorithms(unittest.TestCase):

  def test_displacement(self):
    """Test out my distance algorithm with hand calcs.

    TODO: Figure out how to just test the distance algorithm, without
          summoning a real series. OR, I could just break unittest
          guidelines and leave the test as-is. I was originally thinking
          of having a whole box of algorithms that I test. And that may
          happen one day. But for now, let us make it easy.
    """
    lon = pd.Series([0.0, 0.0, 0.0])
    lon_ew = pd.Series([0.0, 1.0, 2.0])
    lat = pd.Series([0.0, 0.0, 0.0])
    lat_ns = pd.Series([0.0, 1.0, 2.0])

    disp_ew = distance.spherical_earth_plane_displacement(lat, lon_ew)
    self.assertIsInstance(disp_ew, pd.Series)
    self.assertAlmostEqual(disp_ew.iloc[-1], 6371000 * 1.0 * np.pi / 180)

    disp_ns = distance.spherical_earth_plane_displacement(lat_ns, lon)
    self.assertIsInstance(disp_ns, pd.Series)
    self.assertAlmostEqual(disp_ns.iloc[-1], 6371000 * 1.0 * np.pi / 180)


if __name__ == '__main__':
  unittest.main()