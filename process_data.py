from __future__ import print_function
import dolfyn.adv.api as avm
import dolfyn.adp.api as apm
import numpy as np
from os.path import isfile


adv_files = {
    'NREL': 'TTM_NRELvector_Jun2012',
    'PNNL': 'TTM_PNNLvector_Jun2012',
}


def within(dat, range):
    return (range[0] < dat) & (dat < range[1])


def process_adv(files=adv_files, read_raw=None, savefiles=True):
    """Process adv files.

    Parameters
    ----------

    files : dict of {tag: fname} pairs

    read_raw : True, False, None
        Default (None): skip this step unless the output file doesn't
        exist.

    savefiles : boolean
        Default: True, save the data. ``False`` is just for testing purposes.
    """

    for tag, fname in files.iteritems():
        if read_raw or \
           (read_raw is None and
                not isfile('ADV/' + fname + '.h5')):
            dat = avm.read_nortek('ADV/' + fname + '.vec')
            if savefiles:
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
        # Crop the section of the data where the instrument was on the
        # seafloor.
        dat = dat.subset(within(dat.mpltime, dat.props['time_range']))

        print('   cleaning...')
        avm.clean.GN2002(dat.u)
        avm.clean.GN2002(dat.v)
        avm.clean.GN2002(dat.w)

        if savefiles:
            print('   saving...')
            dat.save('ADV/' + fname + '_earth.h5')

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
        if savefiles:
            print('   saving binned data...')
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


def process_awac(savefiles=True, readbin=None):

    if readbin or \
       (readbin is None and not isfile('TTM_AWAC/TTM_AWAC_Jun2012.h5')):
        datawac = apm.read_nortek('TTM_AWAC/TTM_AWAC_Jun2012.wpr')
        datawac = datawac.subset(within(datawac.mpltime, trange))
        datawac.props['coord_sys'] = 'earth'
        #datawac.props['time_label'] = tlabel
        #datawac.props['toff'] = toff
        # From looking at spectra.
        datawac.props['doppler_noise'] = [0.12, 0.12, 0.048]
        datawac.props['fs'] = 1.0
        datawac.props['n_bin'] = 318  # 5min, 20sec.
        if savefiles:
            datawac.save('TTM_AWAC/TTM_AWAC_Jun2012.h5')
    else:
        datawac = apm.load('TTM_AWAC/TTM_AWAC_Jun2012.h5')

    bnr = apm.binner(n_bin=datawac.props['n_bin'], fs=datawac.fs)
    bawac = bnr(datawac)
    bawac.add_data('Spec_vel', bnr.psd(datawac['vel']), 'Spec')
    if savefiles:
        bawac.save('TTM_AWAC/TTM_AWAC_Jun2012_b5m.h5')

    datawac.calc_principal_angle(10)
    # The awac principal angle is 180degrees from the adv one.
    datawac.props['principal_angle'] += np.pi
    apm.earth2principal(datawac)
    if savefiles:
        datawac.save('TTM_AWAC/TTM_AWAC_Jun2012_pax.h5')

    bawac = bnr(datawac)
    bawac.add_data('Spec_vel', bnr.psd(datawac['vel']), 'Spec')
    if savefiles:
        bawac.save('TTM_AWAC/TTM_AWAC_Jun2012_pax_b5m.h5')

    return datawac


if __name__ == '__main__':

    process_adv()
    process_awac()
