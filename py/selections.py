#! /usr/bin/python2

""" Event selection tools """

import sys
sys.path.append('/home/vitaly/work/B0toD0pipi/Analysis/py/lib')

from CutTools import cuts2str, trackCuts, mergeCuts, pionCuts, kaonCuts, union

def DsjCommon():
    """ Common Dsj selections """
    return {
        'mds'           : {'s' : (1.969, 0.012)},
        'pcmsds'        : {'a' : (2.100, 9.999)}
    }

def Dsj2DsGamma():
    """ Dsj -> Ds gamma selections """
    return mergeCuts([DsjCommon(), {
        'mode'          : {'d' : [0]},
        'gam_dsj.e'     : {'a' : (0.300, 9.999)},
        'gam_dsj.costh' : {'a' : (-1.00, 0.800)}
    }])

def Dsj2DsPi0():
    """ Dsj -> Ds pi0 selections """
    return mergeCuts([DsjCommon(), {
        'mode'          : {'d' : [1]},
    }])

def Ds2PhiPi():
    """ Ds+ -> phi pi+ selections """
    dsCuts = {
        'mode' : {'d'  : [0]},            # Ds+ -> phi pi+ mode
        # 'm'    : {'s'  : (1.969, 0.200)}, # Ds mass
        # 'mvec' : {'s'  : (1.020, 0.030)}  # phi mass
    }
    return mergeCuts([dsCuts, pionCuts('h_ds')])

def Ds2KstarK():
    """ Ds+ -> K*0 K+ selections """
    dsCuts = {
        'mode' : {'d'  : [1]},            # Ds+ -> K*0 K+ mode
        # 'm'    : {'s'  : (1.969, 0.200)}, # Ds mass
        # 'mvec' : {'s'  : (0.893, 0.050)}  # K*0 mass
    }
    return mergeCuts([dsCuts, kaonCuts('h_ds')])

def Ds2Ks0K():
    """ Ds+ -> Ks0 K+ selections """
    dsCuts = {
        'mode' : {'d'  : [2]}  # Ds+ -> Ks0 K+ mode
    }
    return mergeCuts([dsCuts, kaonCuts('h_ds')])

def Ds2PhiPiStr():
    return cuts2str(Ds2PhiPi())

def Ds2KstarKStr():
    return cuts2str(Ds2KstarK())

def Ds2Ks0KStr():
    return cuts2str(Ds2Ks0K())

def DsStr():
    """ Complete Ds cuts for modes 0, 1 and 2 """
    return union([Ds2PhiPi(), Ds2KstarK(), Ds2Ks0K()])

def main():
    """ Unit test """
    print(DsStr())

if __name__ == '__main__':
    main()
