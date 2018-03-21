# -*- coding: utf-8 -*-
from __future__ import print_function, division
import os
import matplotlib.pyplot as plt
import numpy as np
import psfex
from astropy.io import fits

try:
    print('psfex.__version__: ', psfex.__version__)
except:
   pass

psf_file = '/Users/rliu/Downloads/test/A2029/A2029_PSFEX.psf'

hdulist = fits.open(psf_file)
hdulist.info()
print(hdulist[0].header)
print(hdulist[1].header)


poldeg =hdulist[1].header['POLDEG1']
print('poldeg: ', poldeg)

psf_samp =hdulist[1].header['PSF_SAMP']
print('psf_samp: ', psf_samp)

data=hdulist[1].data
psf_mask=data['PSF_MASK']

print('len(psf_mask.flat): ', len(psf_mask.flat))
print('psf_mask.shape: ', psf_mask.shape)
print('psf_mask.type:  ', psf_mask.size)


pex = psfex.PSFEx(psf_file)

row=5000
column=5000

psf_image = pex.get_rec(row, column)
fits.writeto('psfex_test.fits',psf_image)
print('psf_image.shape: ', psf_image.shape)

imax=np.argmax(psf_image)
xymax = np.unravel_index(imax, psf_image.shape)
print('Location of maximum value: ',xymax)

plt.figure("psfex",figsize=(8.0, 8.0))


plt.imshow(psf_image, interpolation='nearest')
plt.colorbar()
plt.ylabel('Pixels')
plt.xlabel('Pixels')

filename = os.path.basename(psf_file)
title= filename
plt.title(title)

plotfile='psfex_test.png'
print('Saving: ', plotfile)
plt.savefig(plotfile)
