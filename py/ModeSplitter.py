""" Mode spolitter """

from os import listdir, mkdir
from os.path import isfile, join, exists
from glob import glob

from ROOT import TFile, gSystem, TChain, TTree, gDirectory, TEventList

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from selections import DsStr

tuplePath = '/home/vitaly/work/DsjInc/tuples'

def sigMCFile(ty, st):
    """ Get root file name """
    return glob('/'.join([tuplePath, 'signt', '_'.join(['dsjinc', 'sigmc', 'ty' + ty, 'st' + str(st), '*.root'])]))

class ModeSplitter(object):
    """ Mode Splitted for DsjInc """
    mds = 1.96834 # +- 0.07 MeV

    def __init__(self, name, ty, st, modes):
        """ Constructor """
        self.name = name
        self.ty = ty
        self.st = str(st)
        self.modes = modes
        self.t = {}
        self.vars = {}
        self.getChain()
        self.initVarDicts()

    def initVarDicts(self):
        """ Define variables """
        self.branches = {
        'common' : {  # all modes
            'i' : {
                'exp'   : lambda: self.info.exp,
                'run'   : lambda: self.info.run,
                'evtn'  : lambda: self.info.evtn,
                'mode'  : lambda: self.evt.mode,
                'dsmode': lambda: self.evt.mode_ds,
                'flv'   : lambda: self.evt.flv
            },
            'f' : {
                'm'          : lambda: self.evt.m - self.evt.mds + ModeSplitter.mds,
                'mds'        : lambda: self.evt.mds,
                'pcmds'      : lambda: self.evt.pcmsds,
                'cos_hel_dsj': lambda: self.evt.cos_hel_dsj,
                'mvec'       : lambda: self.evt.mvec,
                'cos_hel_vec': lambda: self.evt.cos_hel_vec
            }
        },
        'commonMC' : {
            'i'  : {
                'h_ds_id'  : lambda: self.mcevt.h_ds_gen.id,
                'h_ds_flag': lambda: self.mcevt.h_ds_gen.flag,
                'ds_flag'  : lambda: self.mcevt.ds_gen.flag,
                'dsj_flag' : lambda: self.mcevt.dsj_gen.flag,
                'tmode'    : lambda: self.mcevt.gam_dsj_gen.id,
                'tdsmode'  : lambda: self.mcevt.gam_dsj_gen.flag
            },
            'iv' : {
                'h_ds_ch'  : lambda: self.mcevt.h_ds_gen.chain,
            }
        },
        'gamDsj' : {
            'f' : {
                'gam_e'     : lambda: self.evt.gam_dsj.e,
                'gam_costh' : lambda: self.evt.gam_dsj.costh
            }
        },
        'gamDsjMC' : {
            # 'i' : {
            #     'gam_id'   : lambda: self.mcevt.gam_dsj_gen.id,
            #     'gam_flag' : lambda: self.mcevt.gam_dsj_gen.flag
            # },
            'iv' : {
                'gam_ch' : lambda: self.mcevt.gam_dsj_gen.chain
            }
        },
        'pi0Dsj' : {
            'f' : {
                'pi0_eg1'   : lambda: min(self.evt.pi0_dsj.eg1, self.evt.pi0_dsj.eg2),
                'pi0_eg2'   : lambda: max(self.evt.pi0_dsj.eg1, self.evt.pi0_dsj.eg2)
            }
        },
        'pi0DsjMC' : {
            'i' : {
                'pi0_id'   : lambda: self.mcevt.pi0_dsj_gen.id,
                'pi0_flag' : lambda: self.mcevt.pi0_dsj_gen.flag
            },
            'iv' : {
                'pi0_ch' : lambda: self.mcevt.pi0_dsj_gen.chain
            }
        },
        'pi+pi-' : {
            'f' : {
                'pip_atckpi' : lambda: self.evt.pip_dsj.atckpi,
                'pip_px'     : lambda: self.evt.pip_dsj.p[0],
                'pip_py'     : lambda: self.evt.pip_dsj.p[1],
                'pip_pz'     : lambda: self.evt.pip_dsj.p[2],
                'pim_atckpi' : lambda: self.evt.pim_dsj.atckpi,
                'pim_px'     : lambda: self.evt.pim_dsj.p[0],
                'pim_py'     : lambda: self.evt.pim_dsj.p[1],
                'pim_pz'     : lambda: self.evt.pim_dsj.p[2]
            }
        },
        'pi+pi-MC' : {
            'i' : {
                'pip_id'   : lambda: self.mcevt.pip_dsj_gen.id,
                'pip_flag' : lambda: self.mcevt.pip_dsj_gen.flag,
                'pim_id'   : lambda: self.mcevt.pim_dsj_gen.id,
                'pim_flag' : lambda: self.mcevt.pim_dsj_gen.flag
            },
            'iv' : {
                'pip_ch' : lambda: self.mcevt.pip_dsj_gen.chain,
                'pim_ch' : lambda: self.mcevt.pim_dsj_gen.chain
            }
        },
        'pi0pi0' : {
            'f' : {
                'pi0lo_eg1' : lambda: min(self.evt.pi0lo_dsj.eg1, self.evt.pi0lo_dsj.eg2),
                'pi0lo_eg2' : lambda: max(self.evt.pi0lo_dsj.eg1, self.evt.pi0lo_dsj.eg2)
            }
        },
        'pi0pi0MC' : {
            'i' : {
                'pi0lo_id'   : lambda: self.mcevt.pi0lo_dsj_gen.id,
                'pi0lo_flag' : lambda: self.mcevt.pi0lo_dsj_gen.flag
            },
            'iv' : {
                'pi0lo_ch' : lambda: self.mcevt.pi0lo_dsj_gen.chain
            }
        },
        'gamDsst' : {
            'f' : {
                'gam_dsst_e'     : lambda: self.evt.gam_dsst.e,
                'gam_dsst_costh' : lambda: self.evt.gam_dsst.costh,
                'dmdsst'         : lambda: self.evt.dmdsst
            }
        },
        'gamDsstMC' : {
            # 'i' : {
            #     'gamDsst_id'   : lambda: self.mcevt.gam_dsst_gen.id,
            #     'gamDsst_flag' : lambda: self.mcevt.gam_dsst_gen.flag
            # },
            'iv' : {
                'gamDsst_ch' : lambda: self.mcevt.gam_dsst_gen.chain
            }
        }
        }

        mdict = {
            0  : ['common', 'gamDsj'],  # Ds gamma
            1  : ['common', 'pi0Dsj'],  # Ds pi0
            2  : ['common', 'pi+pi-'],  # Ds pi+ pi-
            3  : ['common', 'pi0pi0'],  # Ds pi0 pi0
            10 : ['common', 'gamDsj', 'gamDsst'],  # Ds gamma gamma
            11 : ['common', 'pi0Dsj', 'gamDsst'],  # Ds pi0 gamma
            12 : ['common', 'pi+pi-', 'gamDsst'],  # Ds pi+ pi- gamma
            13 : ['common', 'pi0pi0', 'gamDsst'],  # Ds pi0 pi0 gamma
        }

        self.modeDict = {mode : mdict[mode] for mode in self.modes}

    def getBranches(self, mode, mc):
        """ Get branches for a mode """
        ddict = {}
        for key in ['i', 'f', 'iv']:
            array = []
            for d in self.modeDict[mode]:
                if key in self.branches[d]:
                    array = array + [var for var in self.branches[d][key].keys()]
                if mc and (key in self.branches[d + 'MC']):
                    array = array + [var for var in self.branches[d + 'MC'][key].keys()]
            ddict[key] = array
        return ddict

    def getFiller(self, mode, mc):
        """ Get branches for a mode """
        ddict = {}
        for key in ['i', 'f', 'iv']:
            array = []
            for d in self.modeDict[mode]:
                if key in self.branches[d]:
                    array = array + [(var, fcn) for var, fcn in self.branches[d][key].iteritems()]
                if mc and (key in self.branches[d + 'MC']):
                    array = array + [(var, fcn) for var, fcn in self.branches[d + 'MC'][key].iteritems()]
            ddict[key] = array
        return ddict

    def ofile(self):
        """ Output file """
        return '/'.join([tuplePath, 'signt', '_'.join([self.name, 'sigmc', self.ty, 'st' + self.st, 'split']) + '.root'])

    def split(self):
        """ """
        ofile = TFile(self.ofile(), 'RECREATE')
        for mode in self.modeDict.keys():
            self.makeTree(mode, 'dsj_{}'.format(mode))
        # self.t.Draw('>>evlist', DsStr())
        # evl = TEventList(gDirectory.Get('evlist'))
        # self.t.SetEventList(gDirectory.Get('evlist'))
        for idx, _ in enumerate(self.chain):
            if idx % 10000 == 0:
                print('{} events'.format(idx))
            self.fillEvent(self.evt.mode)
            self.t[self.evt.mode].Fill()
        ofile.Write()
        ofile.Close()

    def makeTree(self, mode, name):
        """ Flat TTree for a given mode """
        br = self.getBranches(mode, True)
        self.t[mode] = TTree(name, name)
        for var in br['i']:
            if var not in self.vars:
                self.vars[var] = np.empty(1, dtype=np.int32)
            self.t[mode].Branch(var, self.vars[var], var + '/I')
        for var in br['f']:
            if var not in self.vars:
                self.vars[var] = np.empty(1, dtype=np.float32)
            self.t[mode].Branch(var, self.vars[var], var + '/F')
        for var in br['iv']:
            if var not in self.vars:
                self.vars[var] = np.empty(9, dtype=np.int32)
            self.t[mode].Branch(var, self.vars[var], var + '[9]/I')

    def fillEvent(self, mode):
        """ Fill common variables """
        filler = self.getFiller(mode, True)
        for var, fcn in filler['i']:
            self.vars[var][0] = fcn()

        for var, fcn in filler['f']:
            self.vars[var][0] = fcn()

        for var, fcn in filler['iv']:
            self.vars[var][:] = fcn()

    def getChain(self):
        """ """
        self.dschain = TChain('ds', 'ds')
        self.chain = TChain('dsj', 'dsj')
        print(sigMCFile(self.ty, self.st))
        for fname in sigMCFile(self.ty, self.st):
            self.chain.Add(fname)
            self.dschain.Add(fname)
        self.chain.GetEvent(0)
        print('{} Dsj candidates'.format(self.chain.GetEntries()))
        self.evt   = self.chain.evt
        self.mcevt = self.chain.mcevt
        self.info  = self.evt.info

def main():
    """ Unit test """
    gSystem.Load('libRecoObj.so')
    gSystem.Load('libdsjdata.so')
    ms = ModeSplitter('dsjinc', 'dsst0', 1, [0, 1, 2, 3, 10, 11, 12, 13])
    ms.split()
    # ms = ModeSplitter('dsjinc', 'dsst1', 1, [0, 1, 2, 3, 10, 11, 12, 13])
    # ms.split()

if __name__ == '__main__':
    main()
