""" """

from glob import glob
import numpy as np

from ROOT import TChain, gSystem

from pdgcode import ids

tuplePath = '/home/vitaly/work/DsjInc/tuples'

def sigMCFile(ty, st):
    """ Get root file name """
    return glob('/'.join([tuplePath, 'signt', '_'.join(['dsjinc', 'sigmc', 'ty' + ty, 'st' + str(st), '*.root'])]))

modesDict = {
    'Dsj+' : {
        0  : set([ids['Ds+'], ids['gamma']]),
        1  : set([ids['Ds+'], ids['pi0']]),
        2  : set([ids['Ds+'], ids['pi+'], ids['pi-']]),
        11 : set([ids['Ds+'], ids['pi0'], ids['gamma']]),
        12 : set([ids['Ds+'], ids['pi+'], ids['pi-'], ids['gamma']]),
    },
    'Dsj-' : {
        0  : set([ids['Ds-'], ids['gamma']]),
        1  : set([ids['Ds-'], ids['pi0']]),
        2  : set([ids['Ds-'], ids['pi+'], ids['pi-']]),
        11 : set([ids['Ds-'], ids['pi0'], ids['gamma']]),
        12 : set([ids['Ds-'], ids['pi+'], ids['pi-'], ids['gamma']]),
    },
    'Ds+' : {
        0 : set([ids['phi'], ids['pi+']]),
        1 : set([ids['K+'] , ids['K*0bar']]),
        2 : set([ids['Ks0'], ids['K+']])
    },
    'Ds-' : {
        0 : set([ids['phi'], ids['pi-']]),
        1 : set([ids['K-'] , ids['K*0']]),
        2 : set([ids['Ks0'], ids['K-']])
    }
}

class GenHepAnalyser(object):
    """ """
    def __init__(self, dstree):
        """ """
        self.chain  = dstree
        self._get = {
            'exp'   : lambda: self.chain.evt.info.exp,
            # 'run'   : lambda: self.chain.evt.info.run,
            'evtn'  : lambda: self.chain.evt.info.evtn,
            'idhep' : lambda: self.chain.mcevt.genhep.idhep,
            'daF'   : lambda: self.chain.mcevt.genhep.daF,
            'daL'   : lambda: self.chain.mcevt.genhep.daL,
        }
        self.ddata = {key: [] for key in ['exp', 'evtn', 'id', 'mode']}
        self.run()

    def get(self, key):
        """ """
        assert(key in self._get)
        return self._get[key]()

    def run(self):
        """ Event loop """
        curEvt = (-1, -1)
        for idx, _ in enumerate(self.chain):
            if idx % 1000 == 0:
                print('{} events'.format(idx))
            if (self.get('exp'), self.get('evtn')) == curEvt:
                continue
            else:
                curEvt = (self.get('exp'), self.get('evtn'))
            self.findDecay(ids['Ds+'], 'Ds+')
            self.findDecay(ids['Ds-'], 'Ds-')
            self.findDecay(ids['Dsj0+'], 'Dsj+')
            self.findDecay(ids['Dsj1+'], 'Dsj+')
            self.findDecay(ids['Dsj0-'], 'Dsj-')
            self.findDecay(ids['Dsj1-'], 'Dsj-')
        
        self.data = np.empty(len(self.ddata['exp']),
                    dtype=[('exp', np.int32), ('evtn', np.int32), ('id', np.int32), ('mode', np.int32)])
        for key, val in self.ddata.iteritems():
            self.data[key] = val

    def findDecay(self, idhep, key):
        """ Identify mode in the EvtGen table """
        nphep = np.array(self.get('idhep'))
        npdaF = np.array(self.get('daF'))
        npdaL = np.array(self.get('daL'))
        for idx in np.nonzero(nphep == idhep)[0]:
            fsp = set([nphep[i] for i in np.arange(npdaF[idx]-1, npdaL[idx]) if i < 100])
            for mode, fsps in modesDict[key].iteritems():
                if fsp == fsps:
                    if mode == 0 and npdaL[idx] == npdaF[idx] + 2:
                        mode = mode + 10
                    elif mode == 1 and npdaL[idx] == npdaF[idx] + 2:
                        mode = 3
                    elif mode == 11 and npdaL[idx] == npdaF[idx] + 3:
                        mode = 13
                    self.ddata['exp'].append(self.get('exp'))
                    self.ddata['evtn'].append(self.get('evtn'))
                    self.ddata['id'].append(idhep)
                    self.ddata['mode'].append(mode)

def main():
    """ Unit test """
    print(modesDict)
    gSystem.Load('libRecoObj.so')
    gSystem.Load('libdsjdata.so')
    chain = TChain('ds', 'ds')
    for fname in sigMCFile('dsst0', 1):
        chain.Add(fname)
    print('{} Ds candidates'.format(chain.GetEntries()))
    gha = GenHepAnalyser(chain)
    print(gha.data[:10])
    np.save('mctruth.npy', gha.data)

if __name__ == '__main__':
    main()
