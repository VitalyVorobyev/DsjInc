""" Mode spolitter """

from os import listdir, mkdir
from os.path import isfile, join, exists
from glob import glob

from ROOT import TFile, gSystem, TChain, TTree

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from lvect import Vect, LVect

tuplePath = '/home/vitaly/work/DsjInc/tuples'

ids = {
        'dsj0+'  :  10431,
        'dsj0-'  : -10431,
        'dsj1+'  :  20433,
        'dsj1-'  : -20433,
        'ds+'    :  431,
        'ds-'    : -431,
        'dsst+'  :  433,
        'dsst-'  : -433,
        'gamma'  :  22,
        'pi0'    :  111,
        'phi'    :  333,
        'pi+'    :  211,
        'pi-'    : -211,
        'K+'     :  321,
        'K-'     : -321,
        'Kst+'   :  313,
        'Kst-'   : -313,
        'Ks0'    :  310
    }

modeDsjSets = {
        0 : [set([ids['ds'], ids['gamma']]), set([-ids['ds'], ids['gamma']])],
        1 : [set([ids['ds'], ids['pi0']]),   set([-ids['ds'], ids['pi0']])],
        2 : [set([ids['ds'], ids['pi0']]),   set([-ids['ds'], ids['pi0']])],
    }

modeDsSets = {
        0 : [set([ids['phi'], ids['pi+']]), set([ids['phi'], ids['pi-']])],
        1 : [set([ids['ds'], ids['pi0']]),   set([-ids['ds'], ids['pi0']])],
        2 : [set([ids['ds'], ids['pi0']]),   set([-ids['ds'], ids['pi0']])],
    }

def sigMCFile(ty, st):
    """ Get root file name """
    return glob('/'.join([tuplePath, 'signt', '_'.join(['dsjinc', 'sigmc', 'ty' + ty, 'st' + str(st), '*.root'])]))

def Branches(mode):
    """ Set of branches """
    common = {  # all modes
        'i'  : ['exp', 'run', 'evtn', 'mode', 'dsmode', 'flv', 'h_ds_id', 'h_ds_flag', 'tmode', 'tdsmode'],
        'f'  : ['m', 'mds', 'pcmds', 'cos_hel_dsj'],
        'iv' : ['h_ds_ch']
    }

    vec = {  # phi or K*0 fomr Ds
        'i'  : ['h1_vec_id', 'h1_vec_flag', 'h2_vec_id', 'h2_vec_flag'],
        'f'  : ['mvec', 'cos_hel_vec'],
        'iv' : ['h1_vec_ch', 'h2_vec_ch', 'h_ds_ch']
    }

    gamDsj = {  # gamma from Dsj
        'i'  : ['gam_dsj_id', 'gam_dsj_flag'],
        'f'  : ['gam_dsj_e',  'gam_dsj_costh'],
        'iv' : ['gam_dsj_ch']
    }

    pi0Dsj = {  # pi0 from Dsj
        'i'  : ['gam_dsj_id', 'gam_dsj_flag'],
        'f'  : ['pi0_dsj_eg1', 'pi0_dsj_eg2', 'pi0_dsj_p',  'gam_dsj_costh'],
        'iv' : ['pi0_dsj_ch']
        }

    modeDict = {
        0 : [common, vec, gamDsj],  # Ds gamma
        1 : [common, vec, pi0Dsj],  # Ds pi0
        }
    
    return {key : [val for sub in modeDict[mode] for val in sub] for key in common.keys()}

class ModeSplitter(object):
    """ Mode Splitted for DsjInc """
    mds    = 1968.34 # +- 0.07 MeV

    def __init__(self, name, ty, st, modes):
        """ Constructor """
        self.name = name
        self.ty = ty
        self.st = st
        self.modes = modes

    def makeTree(self, mode, name):
        """ Flat TTree for a given mode """
        br = Branches(mode)
        self.t = TTree(name, name)
        self.vars = {}
        for var in br['i']:
            self.vars[var] = int(0)
            self.t.Branch(var, self.vars[var], var + '/I')
        for var in br['f']:
            self.vars[var] = float(0)
            self.t.Branch(var, self.vars[var], var + '/D')
        for var in br['iv']:
            self.vars[var] = np.empty(9, dtype=np.int32)
            self.t.Branch(var, self.vars[var], var + '[9]/D')

    def fillCommon(self):
        """ Fill common variables """
        # 'i'  : ['exp', 'run', 'evtn', 'mode', 'dsmode', 'flv', 'h_ds_id', 'h_ds_flag', 'tmode'],
        # 'f'  : ['m', 'mds', 'pcmds', 'cos_hel_dsj'],
        # 'iv' : ['h_ds_ch']
        # Integer branches
        self.vars['exp']    = self.info.exp
        self.vars['run']    = self.info.run
        self.vars['evtn']   = self.info.evtn
        self.vars['mode']   = self.evt.mode
        self.vars['dsmode'] = self.evt.mode_ds
        self.vars['flv']    = self.evt.flv

        # MC
        self.vars['h_ds_id']   = self.mcevt.h_ds_gen.id
        self.vars['h_ds_flag'] = self.mcevt.h_ds_gen.flag
        
        # Float branches
        self.vars['m']     = self.evt.m - self.evt.mds + ModeSplitter.mds
        self.vars['mds']   = self.evt.mds
        self.vars['pcmds'] = self.evt.pcmsds
        self.vars['cos_hel_dsj'] = self.evt.cos_hel_dsj
        
        # MC
        self.vars['h_ds_ch'][:] = self.mcevt.h_ds_gen.ch

    def find

    def getChain(self):
        """ """
        self.intree = TChain('dsj', 'dsj')
        for fname in sigMCFile(self.ty, self.st):
            self.intree.Add(fname)
        print('{} Dsj candidates'.format(self.intree.GetEntries()))
        self.evt   = self.intree.evt
        self.mcevt = self.intree.mcevt
        self.info  = self.evt.info

    # def splitSigMC(self):
    #     """ Split signal MC """
    #     ofile = TFile('/'.join([tuplePath, 'signt', '_'.join([self.name, 'sigmc', ty, 'st' + str(st), 'split']) + '.root']), 'RECREATE')
    #     otree = {key : dsj.CloneTree(0) for key in self.modes}
    #     for key, tree in otree.iteritems():
    #         tree.SetName('dsj_{}'.format(key))
    #     evt = dsj.evt
    #     for idx, _ in enumerate(dsj):
    #         if idx % 100000 == 0:
    #             print('{} events'.format(idx))
    #         if evt.mode in modes:
    #             otree[evt.mode].Fill()
    #     for key, tree in otree.iteritems():
    #         print('mode {:02d} : {:07d} events'.format(key, tree.GetEntries()))
    #     ofile.Write()
    #     ofile.Close()

def main():
    """ Unit test """
    gSystem.Load('libRecoObj.so')
    gSystem.Load('libdsjdata.so')
    ms = ModeSplitter('dsjinc', 'dsUps', 0, [0, 1, 2, 3, 10, 11, 12, 13])
    # ms.splitSigMC()

if __name__ == '__main__':
    main()

# makeSigDirTree()
