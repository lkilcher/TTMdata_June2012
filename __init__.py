"""
This repository holds the data from the original 'TTM' deployment.

It has two ADV files, and one AWAC data file.


"""
import dolfyn.adv.api as avm
import dolfyn.adp.api as apm
import os.path

try:
    package_root = os.path.dirname(os.path.realpath(__file__)) + '/'
except:
    package_root = './'

#package_root = '/Users/lkilcher/tmp/J12/'


def load(tag, coordsys='pax', bin=False, **kwargs):
    """Load a data file from this repository.

    Parameters
    ----------

    tag : string
       The instrument to load. This may be one of:
          NREL
          PNNL

    coordsys : string {'raw', 'earth', 'pax'}
       The coordinate system in which to load the data.

    bin : bool (default: False)
       Whether to load averaged data (only valid for coordsys 'earth'
       and 'pax')

    """
    if tag.upper() == 'AWAC':
        suffix = ''
        if coordsys == 'pax':
            suffix += '_pax'
        if bin:
            suffix += '_b5m'
        return apm.load(package_root +
                        'TTM_AWAC/TTM_AWAC_Jun2012{}.h5'.format(suffix), **kwargs)
    if tag not in ['NREL', 'PNNL']:
        raise Exception("The two data entries (instruments) in "
                        "this 'June2012' repository are 'NREL' and 'PNNL'.")
    if bin:
        if coordsys not in ['earth', 'pax']:
            raise Exception("Binned data is only stored in "
                            "the 'earth' and 'pax' coordinate systems.")
        return avm.load(package_root +
                        'ADV/TTM_{}vector_Jun2012_{}_b5m.h5'.format(tag, coordsys, ), **kwargs)
    else:
        if coordsys in ['earth', 'pax']:
            dat = avm.load(package_root + 'ADV/TTM_{}vector_Jun2012_earth.h5'.format(tag), **kwargs)
            if coordsys == 'pax':
                avm.rotate.earth2principal(dat)
            return dat
        elif coordsys == 'raw':
            return avm.load(package_root + 'ADV/TTM_{}vector_Jun2012.h5'.format(tag), **kwargs)
    raise Exception("Invalid file specification.")
