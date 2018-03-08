# -*- coding: utf-8 -*-
#!/usr/bin/env python
## last modified by Robert Liu at 9/12/2017
import re
import sys
import numpy as np
from astropy.io import fits


if len(sys.argv) != 2:
    print >>sys.stderr, "Usage: python readout_src_2.0.py {source_fits_file} > {catalog_file}"
    exit(1);
srcfits = sys.argv[1]

# Load sources and print all columns
if srcfits=='':
	srcfits = 'src.fits'

d = fits.open('%s' %(srcfits))
data = d[1].data
cols = d[1].columns
header_table = d[1].header

# flags & cols below are just for reference, they will NOT be printed directly
flag_names = (
         "calib_detected",
         "calib_psfCandidate",
         "calib_psfUsed",
         "calib_psfReserved",
         "flags_negative",     #Added according to newer DMstack version (2017.7.20)
         "deblend_deblendedAsPsf",
         "deblend_tooManyPeaks",
         "deblend_parentTooBig",
         "deblend_masked",
         "deblend_skipped",
         "deblend_rampedTemplate",
         "deblend_patchedTemplate",
         "deblend_hasStrayFlux",
         "base_GaussianCentroid_flag",
         "base_GaussianCentroid_flag_noPeak",
         "base_GaussianCentroid_flag_resetToPeak",
         "base_NaiveCentroid_flag",
         "base_NaiveCentroid_flag_noCounts",
         "base_NaiveCentroid_flag_edge",
         "base_NaiveCentroid_flag_resetToPeak",
         "base_SdssCentroid_flag",
         "base_SdssCentroid_flag_edge",
         "base_SdssCentroid_flag_noSecondDerivative",
         "base_SdssCentroid_flag_almostNoSecondDerivative",
         "base_SdssCentroid_flag_notAtMaximum",
         "base_SdssCentroid_flag_resetToPeak",
         "base_SdssShape_flag",
         "base_SdssShape_flag_unweightedBad",
         "base_SdssShape_flag_unweighted",
         "base_SdssShape_flag_shift",
         "base_SdssShape_flag_maxIter",
         "base_SdssShape_flag_psf",
         "ext_shapeHSM_HsmPsfMoments_flag",
         "ext_shapeHSM_HsmPsfMoments_flag_no_pixels",
         "ext_shapeHSM_HsmPsfMoments_flag_not_contained",
         "ext_shapeHSM_HsmPsfMoments_flag_parent_source",
         "ext_shapeHSM_HsmShapeRegauss_flag",
         "ext_shapeHSM_HsmShapeRegauss_flag_no_pixels",
         "ext_shapeHSM_HsmShapeRegauss_flag_not_contained",
         "ext_shapeHSM_HsmShapeRegauss_flag_parent_source",
         "ext_shapeHSM_HsmShapeRegauss_flag_galsim",
         "ext_shapeHSM_HsmSourceMoments_flag",
         "ext_shapeHSM_HsmSourceMoments_flag_no_pixels",
         "ext_shapeHSM_HsmSourceMoments_flag_not_contained",
         "ext_shapeHSM_HsmSourceMoments_flag_parent_source",
         "base_CircularApertureFlux_3_0_flag",
         "base_CircularApertureFlux_3_0_flag_apertureTruncated",
         "base_CircularApertureFlux_3_0_flag_sincCoeffsTruncated",
         "base_CircularApertureFlux_4_5_flag",
         "base_CircularApertureFlux_4_5_flag_apertureTruncated",
         "base_CircularApertureFlux_4_5_flag_sincCoeffsTruncated",
         "base_CircularApertureFlux_6_0_flag",
         "base_CircularApertureFlux_6_0_flag_apertureTruncated",
         "base_CircularApertureFlux_6_0_flag_sincCoeffsTruncated",
         "base_CircularApertureFlux_9_0_flag",
         "base_CircularApertureFlux_9_0_flag_apertureTruncated",
         "base_CircularApertureFlux_9_0_flag_sincCoeffsTruncated",
         "base_CircularApertureFlux_12_0_flag",
         "base_CircularApertureFlux_12_0_flag_apertureTruncated",
         "base_CircularApertureFlux_17_0_flag",
         "base_CircularApertureFlux_17_0_flag_apertureTruncated",
         "base_CircularApertureFlux_25_0_flag",
         "base_CircularApertureFlux_25_0_flag_apertureTruncated",
         "base_CircularApertureFlux_35_0_flag",
         "base_CircularApertureFlux_35_0_flag_apertureTruncated",
         "base_CircularApertureFlux_50_0_flag",
         "base_CircularApertureFlux_50_0_flag_apertureTruncated",
         "base_CircularApertureFlux_70_0_flag",
         "base_CircularApertureFlux_70_0_flag_apertureTruncated",
         "base_GaussianFlux_flag",
         "base_PixelFlags_flag",
         "base_PixelFlags_flag_offimage",
         "base_PixelFlags_flag_edge",
         "base_PixelFlags_flag_interpolated",
         "base_PixelFlags_flag_saturated",
         "base_PixelFlags_flag_cr",
         "base_PixelFlags_flag_bad",
         "base_PixelFlags_flag_suspect",
         "base_PixelFlags_flag_interpolatedCenter",
         "base_PixelFlags_flag_saturatedCenter",
         "base_PixelFlags_flag_crCenter",
         "base_PixelFlags_flag_suspectCenter",
         "base_PsfFlux_flag",
         "base_PsfFlux_flag_noGoodPixels",
         "base_PsfFlux_flag_edge",
         "base_Variance_flag",
         "base_Variance_flag_emptyFootprint",
         "base_PsfFlux_flag_apCorr",
         "base_GaussianFlux_flag_apCorr",
         "base_ClassificationExtendedness_flag",
        )

colum_names = (
        "id",
        "coord_ra",
        "coord_dec",
        "parent",
        "deblend_nChild",
        "deblend_psfCenter_x",
        "deblend_psfCenter_y",
        "deblend_psfFlux",
        "base_GaussianCentroid_x",
        "base_GaussianCentroid_y",
        "base_NaiveCentroid_x",
        "base_NaiveCentroid_y",
        "base_SdssCentroid_x",
        "base_SdssCentroid_y",
        "base_SdssCentroid_xSigma",
        "base_SdssCentroid_ySigma",
        "base_SdssShape_xx",
        "base_SdssShape_yy",
        "base_SdssShape_xy",
        "base_SdssShape_xxSigma",
        "base_SdssShape_yySigma",
        "base_SdssShape_xySigma",
        "base_SdssShape_x",
        "base_SdssShape_y",
        "base_SdssShape_flux",
        "base_SdssShape_fluxSigma",
        "base_SdssShape_psf_xx",
        "base_SdssShape_psf_yy",
        "base_SdssShape_psf_xy",
        "base_SdssShape_flux_xx_Cov",
        "base_SdssShape_flux_yy_Cov",
        "base_SdssShape_flux_xy_Cov",
        "ext_shapeHSM_HsmPsfMoments_x",
        "ext_shapeHSM_HsmPsfMoments_y",
        "ext_shapeHSM_HsmPsfMoments_xx",
        "ext_shapeHSM_HsmPsfMoments_yy",
        "ext_shapeHSM_HsmPsfMoments_xy",
        "ext_shapeHSM_HsmSourceMoments_x",
        "ext_shapeHSM_HsmSourceMoments_y",
        "ext_shapeHSM_HsmSourceMoments_xx",
        "ext_shapeHSM_HsmSourceMoments_yy",
        "ext_shapeHSM_HsmSourceMoments_xy",
        "ext_shapeHSM_HsmShapeRegauss_e1",
        "ext_shapeHSM_HsmShapeRegauss_e2",
        "ext_shapeHSM_HsmShapeRegauss_sigma",
        "ext_shapeHSM_HsmShapeRegauss_resolution",
        "base_CircularApertureFlux_3_0_flux",
        "base_CircularApertureFlux_3_0_fluxSigma",
        "base_CircularApertureFlux_4_5_flux",
        "base_CircularApertureFlux_4_5_fluxSigma",
        "base_CircularApertureFlux_6_0_flux",
        "base_CircularApertureFlux_6_0_fluxSigma",
        "base_CircularApertureFlux_9_0_flux",
        "base_CircularApertureFlux_9_0_fluxSigma",
        "base_CircularApertureFlux_12_0_flux",
        "base_CircularApertureFlux_12_0_fluxSigma",
        "base_CircularApertureFlux_17_0_flux",
        "base_CircularApertureFlux_17_0_fluxSigma",
        "base_CircularApertureFlux_25_0_flux",
        "base_CircularApertureFlux_25_0_fluxSigma",
        "base_CircularApertureFlux_35_0_flux",
        "base_CircularApertureFlux_35_0_fluxSigma",
        "base_CircularApertureFlux_50_0_flux",
        "base_CircularApertureFlux_50_0_fluxSigma",
        "base_CircularApertureFlux_70_0_flux",
        "base_CircularApertureFlux_70_0_fluxSigma",
        "base_GaussianFlux_flux",
        "base_GaussianFlux_fluxSigma",
        "base_PsfFlux_flux",
        "base_PsfFlux_fluxSigma",
        "base_Variance_value",
        "base_PsfFlux_apCorr",
        "base_PsfFlux_apCorrSigma",
        "base_GaussianFlux_apCorr",
        "base_GaussianFlux_apCorrSigma",
        "base_ClassificationExtendedness_value",
        "footprint",
        )
# flags & cols above are just for reference, they will NOT be printed directly

#print '#' + ' '.join(flags) + ' '.join(cols)
# Print all flag names and column names at the beginning
"""
print '#',
for i in xrange(len(header_table['TFLAG*'])):
    print ''.join(header_table['TFLAG*'][i]),
for i in xrange(len(header_table['TTYPE*'])):
    print ''.join(header_table['TTYPE*'][i]),
print ''
"""

newcols = cols.names
newcols.remove('flags')

vecs = data.field('flags')*1
for i in newcols:
    v=data.field(i)
    vecs = np.hstack((vecs,v[:,None]))

print('\n'.join(' '.join(str(x) for x in row) for row in vecs))
