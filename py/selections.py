#! /usr/bin/python2

""" Event selection tools """

import sys
sys.path.append('/home/vitaly/work/B0toD0pipi/Analysis/py/lib')

from CutTools import cuts2str, trackCuts, mergeCuts

def DsPhiPiCuts():
    """ Ds+ -> phi pi+ selections """
    # pi+ cuts
    h_dsCuts = trackCuts('h_ds',
        (0.000, 0.800),  # K/pi ID
        (0.000, 0.200),  # e ID
         0.2, 1.0        # r and z IP
    )
    # Other cuts
    dsCuts = {
        'mode' : {'d'  : [0]},            # Ds+ -> phi pi+ mode
        'm'    : {'s'  : (1.969, 0.040)}, # Ds mass
        'mvec' : {'s'  : (1.020, 0.010)}  # phi mass
    }
    return mergeCuts([dsCuts, h_dsCuts])

def DsPhiPiSelections():
    """ """
    return cuts2str(DsPhiPiCuts())
