""" Mode spolitter """

from os import listdir, mkdir
from os.path import isfile, join, exists
from glob import glob

from ROOT import TFile, gSystem, TChain, TTree, gDirectory, TEventList

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from selections import DsStr
from GenHepAnalyzer import GenHepAnalyser

tuplePath = '/home/vitaly/work/DsjInc/tuples'

verbLvl = 5
debugLvl = 10
infoLvl = 0

def sigMCFile(ty, st):
    """ Get root file name """
    return glob('/'.join([tuplePath, 'signt', '_'.join(['dsjinc', 'sigmc', 'ty' + ty, 'st' + str(st), '*.root'])]))

class ModeSplitter(object):
    """ Mode Splitter for DsjInc """
    mds = 1.96834 # +- 0.07 MeV

    def __init__(self, name, ty, st, modes, mctruth=None):
        """ Constructor """
        self.DsID = 431
        self.Dsj0ID = 10431
        self.Dsj1ID = 20433

        self.name = name
        self.ty = ty
        self.st = str(st)
        self.modes = modes

        self.getChain()

        if mctruth is None:
            gha = GenHepAnalyser(self.dschain)
            self.mctruth = gha.data
        else:
            self.mctruth = np.load(mctruth)
        self.truth = {
            'idx' : 0, 'exev' : (None, None), # EXp, EVtn
            'mode' : None, 'dsmode' : None}
        
        self.t = {}
        self.vars = {}
        self.initVarDicts()

    def setMCTruth(self):
        """ Find out Ds and Dsj modes in an event """
        if self.truth['exev'] == (self.info.exp, self.info.evtn):
            return
        self.truth['exev'] = (self.info.exp, self.info.evtn)
        # print(self.truth['exev'])
        print(self.mctruth[self.truth['idx']])
        print((self.info.exp, self.info.evtn))
        exp, evtn = self.mctruth[self.truth['idx']]['exp'], self.mctruth[self.truth['idx']]['evtn']
        assert((self.info.exp, self.info.evtn) == (exp, evtn))
        self.truth['mode'], self.truth['dsmode'] = -1, -1
        while ((self.mctruth[self.truth['idx']]['exp'],
                self.mctruth[self.truth['idx']]['evtn']) == (exp, evtn)) and (self.truth['idx'] < len(self.mctruth)):
            self.truth['idx'] = self.truth['idx'] + 1
            if abs(self.mctruth[self.truth['idx']]['id']) == self.DsID:
                self.truth['dsmode'] = self.mctruth[self.truth['idx']]['mode']
            elif abs(self.mctruth[self.truth['idx']]['id']) == self.Dsj0ID:
                self.truth['mode'] = self.mctruth[self.truth['idx']]['mode']
            elif abs(self.mctruth[self.truth['idx']]['id']) == self.Dsj1ID:
                self.truth['mode'] = self.mctruth[self.truth['idx']]['mode'] + 1000
        
    def initVarDicts(self):
        """ Define variables """
        self.branches = {
        'common' : {  # all modes
            'i' : {
                'exp'   : lambda: self.info.exp,
                # 'run'   : lambda: self.info.run,
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
        'commonMC' : {  # all modes MC info
            'i'  : {
                'h_ds_id'  : lambda: self.mcevt.h_ds_gen.id,
                'h_ds_flag': lambda: self.mcevt.h_ds_gen.flag,
                'ds_flag'  : lambda: self.mcevt.ds_gen.flag,
                'dsj_flag' : lambda: self.mcevt.dsj_gen.flag,
                'tmode'    : lambda: self.truth['mode'],
                'tdsmode'  : lambda: self.truth['dsmode']
            },
            'iv' : {
                'h_ds_ch'  : lambda: self.mcevt.h_ds_gen.chain,
            }
        },
        'gamDsj' : {  # Dsj -> Ds _gamma_ X
            'f' : {
                'gam_e'     : lambda: self.evt.gam_dsj.e,
                'gam_costh' : lambda: self.evt.gam_dsj.costh
            }
        },
        'gamDsjMC' : {  # Dsj -> Ds _gamma_ X MC info
            # 'i' : {
            #     'gam_id'   : lambda: self.mcevt.gam_dsj_gen.id,
            #     'gam_flag' : lambda: self.mcevt.gam_dsj_gen.flag
            # },
            'iv' : {
                'gam_ch' : lambda: self.mcevt.gam_dsj_gen.chain
            }
        },
        'pi0Dsj' : {  # Dsj -> Ds _pi0_ X
            'f' : {
                'pi0_eg1'   : lambda: min(self.evt.pi0_dsj.eg1, self.evt.pi0_dsj.eg2),
                'pi0_eg2'   : lambda: max(self.evt.pi0_dsj.eg1, self.evt.pi0_dsj.eg2)
            }
        },
        'pi0DsjMC' : {  # Dsj -> Ds _pi0_ X MC info
            'i' : {
                'pi0_id'   : lambda: self.mcevt.pi0_dsj_gen.id,
                'pi0_flag' : lambda: self.mcevt.pi0_dsj_gen.flag
            },
            'iv' : {
                'pi0_ch' : lambda: self.mcevt.pi0_dsj_gen.chain
            }
        },
        'pi+pi-' : {  # Dsj -> Ds _pi+ pi-_
            'f' : {
                'pip_atckpi' : lambda: self.evt.pip_dsj.atckpi,
                'pip_px'     : lambda: self.evt.pip_dsj.p[0],
                'pip_py'     : lambda: self.evt.pip_dsj.p[1],
                'pip_pz'     : lambda: self.evt.pip_dsj.p[2],
                'pim_atckpi' : lambda: self.evt.pim_dsj.atckpi,
                'pim_px'     : lambda: self.evt.pim_dsj.p[0],
                'pim_py'     : lambda: self.evt.pim_dsj.p[1],
                'pim_pz'     : lambda: self.evt.pim_dsj.p[2],
                'mchs'       : lambda: self.evt.mchildren
            }
        },
        'pi+pi-MC' : {  # Dsj -> Ds _pi+ pi-_ MC info
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
        'pi0pi0' : {  # Dsj -> Ds _pi0 pi0_
            'f' : {
                'pi0lo_eg1' : lambda: min(self.evt.pi0lo_dsj.eg1, self.evt.pi0lo_dsj.eg2),
                'pi0lo_eg2' : lambda: max(self.evt.pi0lo_dsj.eg1, self.evt.pi0lo_dsj.eg2),
                'mchs'      : lambda: self.evt.mchildren
            }
        },
        'pi0pi0MC' : {  # Dsj -> Ds _pi0 pi0_ MC info
            'i' : {
                'pi0lo_id'   : lambda: self.mcevt.pi0lo_dsj_gen.id,
                'pi0lo_flag' : lambda: self.mcevt.pi0lo_dsj_gen.flag
            },
            'iv' : {
                'pi0lo_ch' : lambda: self.mcevt.pi0lo_dsj_gen.chain
            }
        },
        'gamDsst' : {  # Dsj -> _Ds*_ X
            'f' : {
                'gam_dsst_e'     : lambda: self.evt.gam_dsst.e,
                'gam_dsst_costh' : lambda: self.evt.gam_dsst.costh,
                'dmdsst'         : lambda: self.evt.dmdsst,
                'mchs'           : lambda: self.evt.mchildren
            }
        },
        'gamDsstMC' : {  # Dsj -> _Ds*_ X MC info
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
            self.setMCTruth()
            # if idx == 10:
            #     break
            if idx % 100 == 0:
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
        if verbLvl > debugLvl:
            print('fillEvent')
        filler = self.getFiller(mode, True)
        for var, fcn in filler['i']:
            if verbLvl > debugLvl:
                print(var)
            self.vars[var][0] = fcn()

        for var, fcn in filler['f']:
            if verbLvl > debugLvl:
                print(var)
            self.vars[var][0] = fcn()

        for var, fcn in filler['iv']:
            if verbLvl > debugLvl:
                print(var)
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
    ms = ModeSplitter('dsjinc', 'dsst0Test', 0, [0, 1, 2, 3, 10, 11, 12, 13], 'mctruth.npy')
    ms.split()
    # ms = ModeSplitter('dsjinc', 'dsst1', 1, [0, 1, 2, 3, 10, 11, 12, 13])
    # ms.split()

if __name__ == '__main__':
    main()
