June 2012 Admiralty Head TTM Dataset
============

This is a repository of turbulence data measured at Admiralty
Head, in Admiralty Inlet (Puget Sound) in June of 2012. The
measurements were made using Inertial Motion Unit (IMU) equipped
Acoustic Doppler Velocimeters (ADVs) mounted on Tidal Turbulence
Mooring's (TTMs).

License
----------
 <a rel="license"
 href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative
 Commons License" style="border-width:0"
 src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />
This work is licensed under a <a rel="license"
href="http://creativecommons.org/licenses/by/4.0/">Creative Commons
Attribution 4.0 International License</a>. A significant amount of
effort has gone into documenting the data and making it publicly
accessible alongside the software tools that we use to work with
it. We believe this process dramatically improves data quality and
usefulness, as well as adding to the well of public knowledge. If you
find this data useful, we kindly request that you let us know by
emailing one of the data's authors. If this data is a major part of a
publication we appreciate the opportunity to be considered for
co-authorship.

Data Summary
---------

The TTM is a compliant mooring designed to position an ADV above the
seafloor to make mid-depth turbulence measurements. The inertial
measurements from the IMU are used in post-processing to remove
mooring motion.

In this dataset each TTM was deployed with two ADV-IMUs. The 'top' ADV
head was positioned 0.5m above the 'bottom' ADV head. The TTMs were
placed in 58 meters [m] of water and the ADVs were 10 m above the
seafloor. For additional details on the data itself, including diagrams and
photos of the TTM,
see
[Kilcher et.al. (2016)][Kilcher++2016],
[Harding et.al. (2017)][Harding++2017],
and [Kilcher et.al. (2017)][Kilcher++2017].


### TTM

Position: 48.1515 N, 122.6858 W

Duration: 2012-06-12 18:15 to 2012-06-14 14:41 (local time)

'Installing' the data
----------

The data is not actually contained within the repository because the
files are too large to be managed by `git`. Instead, the raw
data is stored on
the [MHK Data Repository](http://mhkdr.openei.org/), and this
repository includes tools for downloading and processing the source
data files stored there [[NREL 2015][ttmdata2012]].

This repository requires [Python 2.7](https://docs.python.org/2/), and
the [DOLfYN](https://lkilcher.github.io/dolfyn/) package (>= version
0.8). Assuming you have a functioning and up-to-date version of the
former installed, the latter can be installed by doing:

    $ pip install dolfyn

Once you have DOLfYN installed, you can download and process the data
that this repository holds by simply doing:

    $ python setup_data.py

This _will take some time_, and also about 8GB of hard disk
space. It will first download the source data files
(`TTM###_ADV*_June2012.vec`), then process those source files into
several different versions of each source data file.

Data File Info
------

There are multiple source files within this dataset, which is data
from an individual instrument. For each source data file, the
`<base_name>` is the filename prefix of the source (`.vec`) file. From
this source file, the `process_adv.py` script generates a collection
of processed data files. Each of these data files is likely to be
useful for distinct purposes.

All hdf5 files (`.h5` ending) can be read directly by the DOLfYN library's
'load' function (e.g., `dolfyn.adv.api.load(<base_name>.h5)`), or
using other hdf5 I/O tools
(e.g., [HDFView](http://support.hdfgroup.org/products/java/hdfview/)).

### `<base_name>.vec`

These are the full binary source data files (Nortek format). For information on
this data format see Nortek's 'System Integration Manual' available
at: http://www.nortek-as.com/en/support/application-development

### `<base_name>.h5`

These files contain a 'lightly processed' version of the raw data in
hdf5 format. 

### `<base_name>_earth.h5`

These files contain the motion-corrected data in the earth's ENU
coordinate system. The `vel` attribute (3 by $N_t$ vector time-series)
has been motion corrected according to `vel = velraw +
velmot`, where `velmot = velrot + velacc`. The `velraw` attribute is
also included in the dataset.

### `<base_name>_earth.mat`

These files contain the same data that is in the `<base_name>_earth.h5`
file, in Matlab format.

### `<base_name>_Average5min.csv`

These are simple 'comma separated value' (csv) files containing 5
minute averages of the 3-components of the earth frame velocity (ENU),
and the turbulence intensity.

### `<base_name>_earth_b5m.h5`

These files contain data files that have been 'binned' to compute
various turbulence statistics. This includes mean velocities, Reynolds
stresses, turbulent kinetic energy (tke), tke spectra, and so on.

### `<base_name>_pax_b5m.h5`

These files contain data files that have been rotated into a
'principal axes' coordinate system before they are 'binned'. The
principal axes are aligned with the dominant direction of the tidal
flow (positive velocities are in the direction of ebb). Thus, this
data is in an 'ebb-cross-up' coordinate system; where the 'cross'
direction is chosen to maintain a right-handed coordinate system. The
`props['principal_angle']` attribute of each data set indicates the
direction of ebb (generally to the WNW). All of the same statistics
are present in these files as in the `<base_name>_earth_b5m.h5` files,
but they are in this 'principal' coordinate system.

Units
-----

- Velocity data (vel, velrot, velacc) is in m/s.
- Acceleration (Accel) data is in m/s^2.
- Angular rate (AngRt) data is in rad/s.
- Time is in MatPlotLib datenum (mpltime) format for hdf5 files, and
  in Matlab datenum format for Matlab files.
- The components of all vectors are in 'ENU' (East-North-Up)
  orientation unless specified otherwise. That is, the first index is
  True East, the second is True North, and the third is Up (vertical).
- All other quantities are in the units defined in the Nortek Manual.

Example Usage
-----------

Once the data has been downloaded and processed, make sure this
package is on the Python search path by adding it's *parent folder* to
the
[Python search path](https://docs.python.org/2/tutorial/modules.html). Then,
data can be loaded from it by simply doing:

    import TTMdata_June2012 as j12

    dat = j12.load('adv-nrel')

References
---------------

Kilcher, L.; Thomson, J.; Talbert, J. and DeKlerk, A. (2016)
"Measuring Turbulence from Moored Acoustic Doppler Velocimeters",
National Renewable Energy Lab, [NREL/TP-5000-62979][Kilcher++2016].

[Kilcher++2016]: http://www.nrel.gov/docs/fy16osti/62979.pdf

Harding, S; Kilcher, L.; and Thomson, J. (2017)
"Turbulence Measurements from Compliant Moorings - Part I: Motion Characterization"
Journal of Atmospheric and Oceanic Technology,
doi:
[10.1175/JTECH-D-16-0189.1](http://dx.doi.org/10.1175/JTECH-D-16-0189.1).

[Harding++2017]: http://dx.doi.org/10.1175/JTECH-D-16-0189.1

Kilcher, L.; Thomson, J.; Harding, S; and Nylund, S. (2017)
"Turbulence Measurements from Compliant Moorings - Part II: Motion Correction"
Journal of Atmospheric and Oceanic Technology,
doi:
[10.1175/JTECH-D-16-0213.1](http://dx.doi.org/10.1175/JTECH-D-16-0213.1).

[Kilcher++2017]: http://dx.doi.org/10.1175/JTECH-D-16-0213.1

National Renewable Energy Laboratory. (2015). Admiralty Inlet
Hub-Height Turbulence Measurements from June 2012 [data
set]. Retrieved
from [https://mhkdr.openei.org/submissions/49][ttmdata2012].
doi: [10.15473/1245824](http://dx.doi.org/10.15473/1245824).

[ttmdata2012]: https://mhkdr.openei.org/submissions/49
