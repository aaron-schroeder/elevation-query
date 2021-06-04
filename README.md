# elevation-query

> Python library for getting elevation data from GPS coordinates.

<!--[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)-->
[![License](http://img.shields.io/:license-mit-blue.svg)](http://badges.mit-license.org)

---

## Table of Contents                                                                    
- [Background](#background)
- [Introduction](#introduction)
- [Dependencies and Installation](#dependencies-and-installation)
  - [Base Installation](#base-installation)
  - [Extra: Elevation values from Google Maps API](#extra-elevaton-values-from-google-maps-api)
  - [Extra: Elevation values from `.img` and `.geotiff` files](#extra-elevation-values-from-img-and-geotiff-files)
  - [Possible future data sources](#possible-future-data-sources)
- [Example](#example) <!-- - [Project Status](#project-status) -->
- [Contact](#contact)
- [License](#license)


---

## Background

This project originated as the part of my 
[spatialfriend package](https://github.com/aaron-schroeder/spatialfriend) that
retrieved elevation coordinates from various sources locally and around the web.
Lately, I've  been interested in keeping my work in more self-contained modules with 
lighter dependencies, so I split it out.

---

## Introduction

"How high up do you think we are right now?"

There are high-quality models of the Earth's surface out there. From those models,
it's possible to generate so-called "digital elevation models" (DEMs), which represent
the elevation above sea level at any point within the geographic bounds of the model.
And when you record an activity with a GPS-enabled device, you'll get (at the very 
least) a series of coordinates representing your horizontal position on the Earth.
Combine those two sources of data, and you can find out your elevation at each point
along your route. 

The `elevation-query` package attempts to bridge the gap between GPS locations and
elevation data. Give it a series of (lat, lon) coordinates, and it will give you a series
of elevation coordinates. I don't like to trust just one source of truth, so I provide multiple
sources of elevation. That way you can compare and contrast. The National Map, Google Maps,
open-elevation, and even your own data files. Compare them all. See how they work for you.
You're in charge, buster.

*What about Strava's elevation data, and Garmin's, and ... ?* I don't know where they 
get that stuff, and they love to be opaque about their data sources and algorithms. I don't
trust what I don't understand. I figured I could get my hands on better stuff anyways.

*What about my GPS device's elevation?* A constellation of satellites is trying to 
triangulate your elevation from outer space. The vertical accuracy of these satellites is
abysmal. You might shouldn't look at that data at all.

*What about my high end barometric altimeter?* From what I've seen, those work ok. Unless
the weather changes during your hike, altering the barometric pressure without you climbing.
Or if you fail to calibrate it. Also, I don't own one, and I'm looking to improve my own 
station in life!

There are limitations here that cannot be overcome by this package alone. Even on a
perfectly accurate model of the Earth, with every little detail modeled down to a hair's
breadth, you will not get accurate elevation coordinates if your GPS doesn't have you in
the right horizontal location. And even if you have the world's best GPS, you will not get
accurate data from a poorly modeled DEM. The National Map data that this package grants
easy access to...that's a good DEM (where it exists). So if you have good GPS coordinates,
you should get good elevation data from it! The cruel joke is, GPS devices tend to suffer
their worst accuracy in exactly the places where you want it the most: canyons and mountains
where even a small horizontal inaccuracy would make your elevation all wacky. If your GPS
says you're down in the gully, well...the DEM is gonna give you elevation coordinates for
that gully. That's where we need to smooth out your series of elevation coordinates, ruling
out silly elevation gains and losses along your route. Or we could correct your horizontal
position to a known trail (a process called map-matching), and then look up your elevation
coordinates. I am currently working on 
[correcting your improbable elevation time series](https://github.com/aaron-schroeder/pandas-xyz)
("NO I did NOT fall down in the valley for five seconds before climbing back up a sheer cliff"),
and I hope to improve [my map-matching algorithm](https://github.com/aaron-schroeder/mapmatching) 
so you can snap your coordinates back to a real trail.

In the meantime, enjoy these high quality elevation data!!! You don't need a high-end GPS watch
with a barometric altimiter to tell you this stuff - there are workarounds if you are inspired.

---

## Dependencies and Installation

### Base Installation

`elevation-query` allows querying of the National Map's 
[Elevation Point Query Service](https://nationalmap.gov/epqs/). This 
service exposes data from the National Map's 1/3 arc-second Digital 
Elevation Model. 1/3 arc-second refers to the data's horizontal 
resolution in terms of degrees; this equates to roughly 30 meters.

`elevation-query` also provides access to the 
[open-elevation](https://open-elevation.com/) REST API through a similar interface.
This is not recommended, because the API has become overloaded as more and more users
have discovered it. The National Map's reliable REST API should provide superior
performance and data, as long as you are looking for coordinates in the U.S.

<!-- open-elevation also lets you download other data from the web (SRTM etc)
and self-host your own service. From the looks of the Github repo, the download process
might not be working anymore. [There's another updated fork here](https://github.com/Developer66/open-elevation),
I think...kind of a mess. I honestly have not dug in too deep, because the elevation 
service from The National Map has been suiting my needs just fine. -->

[requests](https://pypi.org/project/requests/) is required for the 
base installation.

To install (since I am not on pypi yet), first clone this repo.
```
git clone https://github.com/aaron-schroeder/elevation-query.git
```
Now you have a local version of this package that you can install with `pip`
(the `setup.py` file is configured to make this work).

Activate whatever virtual environment where you wish to install `query`,
and then:
```
pip install ${local_path_to_elevation-query_dir}
```

### Extra: Elevation values from Google Maps API

Google Maps provides access to its Elevation API, but you must provide
your own API Key. Google will charge you if you exceed the number of free
requests in a month. Use at your own risk!

[Google Maps](https://github.com/googlemaps/google-maps-services-python)
and [NumPy](http://www.numpy.org/) are required.

To install the extra requirements, follow the [base installation](#base-installation)
instructions with this slight modification:
```
pip install -e ${local_path_to_elevation-query_dir}[google]
```

### Extra: Elevation values from `.img` and `.geotiff` files

`elevation-query` allows querying of user-owned `.img` and `.geotiff` files
that contain elevation data. Such files are available from 
[the National Map's download page](https://apps.nationalmap.gov/downloader).

:warning: Note :warning: this package extra requires [`rasterio`](https://rasterio.readthedocs.io/en/latest/)
and [`pyproj`](https://pyproj4.github.io/pyproj/stable/), which
depend on some heavy-duty geospatial libraries being installed on your computer. 
I cannot cover how to get them here, as the install processes are system-dependent. Consult 
[`rasterio`](https://rasterio.readthedocs.io/en/latest/installation.html) and
[`pyproj`](https://pyproj4.github.io/pyproj/stable/installation.html) documentation 
to get these set up (yes, that's me punting).

To install the extra requirements, follow the [base installation](#base-installation)
instructions with this slight modification:
```
pip install -e ${local_path_to_elevation-query_dir}[local]
```

### Possible future data sources

#### [Open Topo Data](https://www.opentopodata.org/)

Something new. I am still investigating it.

You can host it yourself or use the free public API.

"The public API has a number of open DEM datasets loaded, including a 30m global dataset, 
the 25m EU-DEM dataset for Europe, and the 10m NED dataset for the US."

---

## Example

```python
import query

latlons = [
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

# Each of the following query functions will return
# your elevation values in meters.

# Only the first two come with the base installation.
elevs_eqps = query.national_map_epqs(latlons)

# Usually, this is very slow, or fails altogether...
elevs_oe = query.open_elevation(latlons)

# Make sure your latlons are within the horizontal bounds of your
# elevation data files first!
elevs_1m = query.national_map_1m(latlons, 'data.tif')  # .img files work too

# Need your own gmaps API key. Be careful and keep it
# from being visible on the web.
from config import user_gmaps_key
elevs_google = query.google(latlons, user_gmaps_key)
```

---

## Project Status

Good to go. Not sure if I feel like it makes sense to put on PyPi though.

### Future Work

 - Generate series of GPS points to compare elevation datasets with each other,
   and test the effect of smoothing with `pandas-xyz` algorithms.

---

## Contact

Reach out to me at one of the following places!

- Website: [trailzealot.com](https://trailzealot.com)
- LinkedIn: [linkedin.com/in/aarondschroeder](https://www.linkedin.com/in/aarondschroeder/)
- Twitter: [@trailzealot](https://twitter.com/trailzealot)
- Instagram: [@trailzealot](https://instagram.com/trailzealot)
- GitHub: [github.com/aaron-schroeder](https://github.com/aaron-schroeder)

---

## License

[![License](http://img.shields.io/:license-mit-blue.svg)](http://badges.mit-license.org)

This project is licensed under the MIT License. See
[LICENSE](https://github.com/aaron-schroeder/py-activityreaders/blob/master/LICENSE)
file for details.
