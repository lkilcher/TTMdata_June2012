#!/usr/bin/python
from __future__ import print_function
try:
    from urllib.request import urlopen
except:
    from urllib import urlopen

import os.path as path
import shutil
import hashlib


try:
    thisdir = path.dirname(path.realpath(__file__))
except NameError:
    thisdir = './'


def sha(fname):
    h = hashlib.sha256()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


class Finf(object):

    def __init__(self, fname, url, size, hash=None):
        self.fname = fname
        self.url = url
        self.size = size
        self.hash = hash

    def checkhash(self, ):
        if self.hash is None:
            return True
        return self.hash == sha(self.fname)


mhkdr = 'https://mhkdr.openei.org/files/'
# (fname, url, filesize, hash)
FILEINFO = [
    Finf('ADV/TTM_NRELvector_Jun2012.vec',
         mhkdr + '49/AdmiraltyInlet_June2012.vec',
         678471678, 'cc077c26175887e8'),

    Finf('ADV/TTM_PNNLvector_Jun2012.vec',
         'https://www.dropbox.com/s/k470ncq7r5jthhz/TTM_PNNLvector_Jun2012.vec?dl=1',
         147462928, '8ea62d15c2ac07c8'),

    Finf('TTM_AWAC/TTM_AWAC_Jun2012.wpr',
         'https://www.dropbox.com/s/uydsz1sy3dpgzrr/TTM_AWAC_Jun2012.wpr?dl=1',
         56513982, '5762067d9e1bed5e'),

]


def checkfile(finf, ):
    if not path.isfile(finf.fname):
        return False
    if not path.getsize(finf.fname) == finf.size:
        print("Size of local file '{}' is wrong. Redownloading..."
              .format(finf.fname))
        return False
    if not finf.checkhash():
        print("Secure hash of local file '{}' is wrong. Redownloading..."
              .format(finf.fname))
        return False
    return True


def retrieve(finf):
    response = urlopen(finf.url)
    with open(thisdir + '/' + finf.fname, 'wb') as f:
        shutil.copyfileobj(response, f)


def main(test_only=False):
    for finf in FILEINFO:
        if not checkfile(finf):
            if test_only:
                continue
            print("Downloading '{}'... ".format(finf.fname), end='')
            retrieve(finf)
            if not finf.checkhash():
                raise Exception('Secure hash check failed!')
            print("Done.")
        else:
            print("File '{}' already exists.".format(finf.fname))


if __name__ == '__main__':
    main()
