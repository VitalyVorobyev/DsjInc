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

ids = {
        'Dsj0+'  :  10431,
        'Dsj0-'  : -10431,
        'Dsj1+'  :  20433,
        'Dsj1-'  : -20433,
        'Ds+'    :  431,
        'Ds-'    : -431,
        'Ds*+'   :  433,
        'Ds*-'   : -433,
        'gamma'  :  22,
        'pi0'    :  111,
        'phi'    :  333,
        'pi+'    :  211,
        'pi-'    : -211,
        'K+'     :  321,
        'K-'     : -321,
        'K*0'    :  313,
        'K*0bar' : -313,
        'Ks0'    :  310
    }

modesDict = {
    'Dsj' : {
        0 : [set([ids['Ds+'], ids['gamma']]), set([ids['Ds-'], ids['gamma']])],
        1 : [set([ids['Ds+'], ids['pi0']]),   set([ids['Ds-'], ids['pi0']])],
        2 : [set([ids['Ds+'], ids['pi0']]),   set([ids['Ds-'], ids['pi0']])]
    },
    'Ds' : {
        0 : [set([ids['phi'], ids['pi+']]), set([ids['phi'],    ids['pi-']])],
        1 : [set([ids['K*0'], ids['K-']]),  set([ids['K*0bar'], ids['K+']])],
        2 : [set([ids['Ks0'], ids['K+']]),  set([ids['Ks0'],    ids['K-']])]
    }
}

def sigMCFile(ty, st):
    """ Get root file name """
    print('/'.join([tuplePath, 'signt', '_'.join(['dsjinc', 'sigmc', 'ty' + ty, 'st' + str(st), '*.root'])]))
    return glob('/'.join([tuplePath, 'signt', '_'.join(['dsjinc', 'sigmc', 'ty' + ty, 'st' + str(st), '*.root'])]))

def Branches(mode):
    """ Set of branches """
    common = {  # all modes
        'i'  : ['exp', 'run', 'evtn', 'mode', 'dsmode', 'flv', 'h_ds_id', 'h_ds_flag', 'tmode', 'tdsmode'],
        'f'  : ['m', 'mds', 'pcmds', 'cos_hel_dsj'],
        'iv' : ['h_ds_ch']
    }

    vec = {  # phi or K*0 fomr Ds
        # 'i'  : ['h1_vec_id', 'h1_vec_flag', 'h2_vec_id', 'h2_vec_flag'],
        'f'  : ['mvec', 'cos_hel_vec'],
        # 'iv' : ['h1_vec_ch', 'h2_vec_ch', 'h_ds_ch']
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
    mds = 1968.34 # +- 0.07 MeV

    def __init__(self, name, ty, st, modes):
        """ Constructor """
        self.name = name
        self.ty = ty
        self.st = st
        self.modes = modes
        self.getChain()

    def split(self):
        """ """
        ofile = TFile('/'.join([tuplePath, 'signt', '_'.join([self.name, 'sigmc', ty, 'st' + str(st), 'split']) + '.root']), 'RECREATE')
        self.makeTree(0, 'dsj_0')
        self.t.Draw('>>evlist', DsStr())
        # evl = TEventList(gDirectory.Get('evlist'))
        self.t.SetEventList(gDirectory.Get('evlist'))
        for _ in self.t:
            if self.evt.mode != 0:
                continue
            self.fillCommon()
            self.fillVec()
            self.t.Fill()
        ofile.Write()
        ofile.Close()

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
        self.vars['tmode'] = self.findDecay(ids['Dsj0+'], 'Dsj') - self.findDecay(ids['Dsj0-'], 'Dsj')\
                           + 100*self.findDecay(ids['Dsj1+'], 'Dsj') - 100*self.findDecay(ids['Dsj1-'], 'Dsj')
        self.vars['tdsmode'] = self.findDecay(ids['Ds+'], 'Ds') - self.findDecay(ids['Ds-'], 'Ds')

        # Float branches
        self.vars['m']     = self.evt.m - self.evt.mds + ModeSplitter.mds
        self.vars['mds']   = self.evt.mds
        self.vars['pcmds'] = self.evt.pcmsds
        self.vars['cos_hel_dsj'] = self.evt.cos_hel_dsj
        
        # MC
        self.vars['h_ds_ch'][:] = self.mcevt.h_ds_gen.ch

    def fillVec(self):
        """ Fill phi or K*0 variables """
        self.vars['mvec'] = self.evt.mvec
        self.vars['cos_hel_vec'] = self.evt.cos_hel_vec

    def findDecay(self, idhep, key):
        """ Identify mode in the EvtGen table """
        nphep = np.array([x for x in self.idhep])
        idxList = np.nonzero(nphep == idhep)
        if not idxList:
            return -1
        decays = []
        for idx in idxList:
            fsp = set([self.idhep[i] for i in np.arange(self.daF[idx], self.daL[idx])])
            for key0, fsp0 in modesDict[key]:
                if fsp in fsp0:
                    decays.append(key0)
        if len(decays) > 1:
            print('several modes found: {}'.format(decays))
        return sum(decays)

    def getChain(self):
        """ """
        self.chain = TChain('dsj', 'dsj')
        print(sigMCFile(self.ty, self.st))
        for fname in sigMCFile(self.ty, self.st):
            self.chain.Add(fname)
        self.intree = self.chain
        self.intree.GetEvent(0)
        print('evt' in dir(self.intree))
        print('{} Dsj candidates'.format(self.intree.GetEntries()))
        self.evt   = self.intree.evt
        self.mcevt = self.intree.mcevt
        self.info  = self.evt.info
        print(dir(self.mcevt))
        self.idhep = self.mcevt.genhep.idhep
        self.daF   = self.mcevt.genhep.daF
        self.daL   = self.mcevt.genhep.daL

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
    ms = ModeSplitter('dsjinc', 'dsst0', 1, [0, 1, 2, 3, 10, 11, 12, 13])
    ms.split()
    # ms.splitSigMC()

if __name__ == '__main__':
    main()

# makeSigDirTree()
