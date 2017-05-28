import dolfyn.adv.api as avm
import dolfyn.adp.api as apm
import filetools as ftbx

pkg_root = ftbx.pkg_root

mhkdr = 'https://mhkdr.openei.org/files/'
# (fname, url, filesize, hash)
FILEINFO = {
    'adv-nrel':
    ftbx.Finf('ADV/TTM_NRELvector_Jun2012.vec',
              mhkdr + '49/AdmiraltyInlet_June2012.vec',
              678471678, 'cc077c26175887e8'),
    'adv-pnnl':
    ftbx.Finf('ADV/TTM_PNNLvector_Jun2012.vec',
              'https://www.dropbox.com/s/k470ncq7r5jthhz/TTM_PNNLvector_Jun2012.vec?dl=1',
              147462928, '8ea62d15c2ac07c8'),
    'awac':
    ftbx.Finf('TTM_AWAC/TTM_AWAC_Jun2012.wpr',
              'https://www.dropbox.com/s/uydsz1sy3dpgzrr/TTM_AWAC_Jun2012.wpr?dl=1',
              56513982, '5762067d9e1bed5e'),
}


def load(tag, coordsys='pax', bin=False, **kwargs):
    """Load a data file from this repository.

    Parameters
    ----------

    tag : string
       The instrument to load. This may be one of:
          adv-nrel
          adv-pnnl
          awac

    coordsys : string {'raw', 'earth', 'pax'}
       The coordinate system in which to load the data.

    bin : bool (default: False)
       Whether to load averaged data (only valid for coordsys 'earth'
       and 'pax')

    """
    finf = FILEINFO[tag]
    if tag.upper() == 'AWAC':
        suffix = ''
        if coordsys == 'pax':
            suffix += '_pax'
        if bin:
            suffix += '_b5m'
        return apm.load(finf.abs_fname +
                        '{}.h5'.format(suffix), **kwargs)
    if bin:
        if coordsys not in ['earth', 'pax']:
            raise Exception("Binned data is only stored in "
                            "the 'earth' and 'pax' coordinate systems.")
        return avm.load(finf.abs_fname +
                        '_{}_b5m.h5'.format(coordsys, ), **kwargs)
    else:
        if coordsys in ['earth', 'pax']:
            dat = avm.load(finf.abs_fname + '_earth.h5', **kwargs)
            if coordsys == 'pax':
                avm.rotate.earth2principal(dat)
            return dat
        elif coordsys == 'raw':
            return avm.load(finf.abs_fname + '.h5', **kwargs)
    raise Exception("Invalid file specification.")


def pull(files_info=FILEINFO.values(), test_only=False):
    for finf in files_info:
        ftbx.retrieve(finf)
