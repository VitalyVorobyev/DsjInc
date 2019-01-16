#! /usr/bin/python2

""" Definition of all variables of analsis """

def fitRange():
    """ Fit ranges """
    return {
        'mDs' : [1.92, 2.02]
    }

def DsPhiPiParams():
    """ The parameters needed for analysis """
    return {
        # 'm'            : (r'm(D_{s}^{0)',     fitRange()['mDs'][0], fitRange()['mDs'][1], 'GeV/c^{2}'),
        'm'            : ('m',     fitRange()['mDs'][0], fitRange()['mDs'][1], 'GeV/c^{2}'),
        # 'h_ds.atckpi'  : (r'atckpi(\pi^{+})', 0., 1., ''),
        # 'h_ds.eid'     : (r'eid(\pi^{+})',    0., 1., ''),
        # 'h_ds.r'       : (r'r(\pi^{+})',     -0.04, 0.04, 'cm'),
        # 'h_ds.z'       : (r'z(\pi^{+})',     -1.50, 1.50, 'cm'),
    }

def DsPhiPiFitParams():
    """ Fit parameters """
    return {
        'mDsMean'  : (1.969, 1.920, 2.020, 'GeV/c^{2}'),
        'mDsWidth' : (0.006, 0.001, 0.010, 'GeV/c^{2}')
    }
