from __future__ import print_function
import dolfyn.adv.api as avm
import dolfyn.adp.api as apm
import numpy as np
from dolfyn.data.time import date2num
import datetime


files = {
    'NREL': 'TTM_NRELvector_Jun2012',
    'PNNL': 'TTM_PNNLvector_Jun2012',
    'AWAC': 'TTM_AWAC_Jun2012 '
}

read_raw = True
#read_raw = False

do_awac = False
do_awac = True


def within(dat, range):
    return (range[0] < dat) & (dat < range[1])

trange = [date2num(datetime.datetime(2012, 6, 12, 18, 15, 0)),
          date2num(datetime.datetime(2012, 6, 14, 14, 41, 0))]

if True:
    for tag, fname in files.iteritems():
        if tag == 'AWAC':
            continue
        if read_raw:
            dat = avm.read_nortek('ADV/' + fname + '.vec')

            dat.props['lon'] = -122.6858
            dat.props['lat'] = 48.1515
            dat.props['height_above_bottom'] = 11  # m
            dat.props['total_water_depth'] = 58  # m
            dat.props['z'] = dat.props['height_above_bottom'] - \
                dat.props['total_water_depth']
            # Declination taken from http://www.ngdc.noaa.gov/geomag-web/#declination
            #  Options: IGRF, 48 09.090', 122 41.149', 2012-06-12
            dat.props['declination'] = 16.79
            if tag == 'NREL':
                dat.props['body2head_rotmat'] = np.eye(3)
                # In meters, in ADV coord-system:
                dat.props['body2head_vec'] = np.array([0.48, -0.07, -0.27])  # m
                # Correct motion (+rotate to earth frame):

            dat.save('ADV/' + fname + '.h5')
        else:
            print('Loading file {}.h5...'.format(fname))
            dat = avm.load('ADV/' + fname + '.h5')

        dat.u[~within(dat.u, [-2.3, 0.5])] = np.NaN
        avm.clean.fillpoly(dat.u, 3, 12)
        dat.v[~within(dat.v, [-1, 1])] = np.NaN
        avm.clean.fillpoly(dat.v, 3, 12)
        dat.w[~within(dat.w, [-1.2, 0.2])] = np.NaN
        avm.clean.fillpoly(dat.w, 3, 12)

        dat.props.pop('declination')
        if tag == 'NREL':
            print('   motion correction + rotating to earth frame...')
            avm.motion.correct_motion(dat)
            # Calculate Euler angles
            dat.pitch, dat.roll, dat.heading = avm.rotate.orient2euler(
                dat.orientmat)
        elif tag == 'PNNL':
            print('   rotating to earth frame...')
            # Rotate to earth frame
            avm.rotate.inst2earth(dat)

        print('   subsetting...')
        # Crop the section of the data where the instrument was on the seafloor.
        dat = dat.subset(within(dat.mpltime, trange))

        print('   cleaning...')
        avm.clean.GN2002(dat.u)
        avm.clean.GN2002(dat.v)
        avm.clean.GN2002(dat.w)

        print('   saving...')
        dat.save('ADV/' + fname + '_earth.h5')

        print('   saving binned data...')
        bnr = avm.TurbBinner(n_bin=5 * 60 * dat.fs, fs=dat.fs)
        bd = bnr(dat)
        if tag == 'NREL':
            bd.add_data('Spec_velrot',
                        bnr.calc_vel_psd(dat.velrot, ),
                        'spec')
            bd.add_data('Spec_velacc',
                        bnr.calc_vel_psd(dat.velacc, ),
                        'spec')
            bd.add_data('Spec_velmot',
                        bnr.calc_vel_psd(dat.velrot + dat.velacc, ),
                        'spec')
            bd.add_data('Spec_velraw',
                        bnr.calc_vel_psd(dat.velraw, ),
                        'spec')
        bd.save('ADV/' + fname + '_earth_b5m.h5')

        print("   saving binned 'principal axes frame' data...")
        # Rotate to the principal coordinate system:
        avm.rotate.earth2principal(dat)
        # Calculate turbulence statistics:
        bd2 = bnr(dat)
        # Save `binned` data.
        if tag == 'NREL':
            bd2.add_data('Spec_velrot',
                         bnr.calc_vel_psd(dat.velrot, ),
                         'spec')
            bd2.add_data('Spec_velacc',
                         bnr.calc_vel_psd(dat.velacc, ),
                         'spec')
            bd2.add_data('Spec_velmot',
                         bnr.calc_vel_psd(dat.velrot + dat.velacc, ),
                         'spec')
            bd2.add_data('Spec_velraw',
                         bnr.calc_vel_psd(dat.velraw, ),
                         'spec')
        bd2.save('ADV/' + fname + '_pax_b5m.h5')

        print("   DONE.")

if do_awac:

    datawac = avm.read_nortek('TTM_AWAC/TTM_AWAC_Jun2012.wpr')
    datawac = datawac.subset(within(datawac.mpltime, trange))
    datawac.props['coord_sys'] = 'earth'
    #datawac.props['time_label'] = tlabel
    #datawac.props['toff'] = toff
    # From looking at spectra.
    datawac.props['doppler_noise'] = {'u': 0.12, 'v': 0.12, 'w': 0.048}
    datawac.props['fs'] = 1.0
    datawac.props['n_bin'] = 318  # 5min, 20sec.
    datawac.save('TTM_AWAC/TTM_AWAC_Jun2012.h5')

    bawac = apm.bin_adcp(datawac, datawac.props['n_bin'])
    bawac.add_data('Suu', bawac.psd(datawac._u))
    bawac.save('TTM_AWAC/TTM_AWAC_Jun2012_b5m.h5')

    datawac.calc_principal_angle(10)
    # The awac principal angle is 180degrees from the adv one.
    datawac.props['principal_angle'] += np.pi
    datawac.earth2principal()
    datawac.save('TTM_AWAC/TTM_AWAC_Jun2012_pax.h5')

    bawac = apm.bin_adcp(datawac, datawac.props['n_bin'])
    bawac.add_data('Suu', bawac.psd(datawac._u))
    bawac.save('TTM_AWAC/TTM_AWAC_Jun2012_pax_b5m.h5')
