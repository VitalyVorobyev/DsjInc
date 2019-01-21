""" """

from glob import glob
import numpy as np

from ROOT import TChain, gSystem

tuplePath = '/home/vitaly/work/DsjInc/tuples'

def sigMCFile(ty, st):
    """ Get root file name """
    return glob('/'.join([tuplePath, 'signt', '_'.join(['dsjinc', 'sigmc', 'ty' + ty, 'st' + str(st), '*.root'])]))

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
    'Dsj+' : {
        0 : set([ids['Ds+'], ids['gamma']]),
        1 : set([ids['Ds+'], ids['pi0']]),
        2 : set([ids['Ds+'], ids['pi+'], ids['pi-']]),
        3 : set([ids['Ds+'], ids['pi0'], ids['pi0']])
    },
    'Dsj-' : {
        0 : set([ids['Ds-'], ids['gamma']]),
        1 : set([ids['Ds-'], ids['pi0']]),
        2 : set([ids['Ds-'], ids['pi+'], ids['pi-']]),
        3 : set([ids['Ds-'], ids['pi0'], ids['pi0']])
    },
    'Ds+' : {
        0 : set([ids['phi'], ids['pi+']]),
        1 : set([ids['K*0'], ids['K+']]),
        2 : set([ids['Ks0'], ids['K+']])
    },
    'Ds-' : {
        0 : set([ids['phi'],    ids['pi-']]),
        1 : set([ids['K*0bar'], ids['K-']]),
        2 : set([ids['Ks0'],    ids['K-']])
    }
}

class GenHepAnalyser(object):
    """ """
    def __init__(self, dstree):
        """ """
        self.chain = dstree
        self.chain.GetEvent(0)
        # print(dir(self.chain))
        # return
        self.idhep = self.chain.mcevt.genhep.idhep
        self.daF = self.chain.mcevt.genhep.daF
        self.daL = self.chain.mcevt.genhep.daL
        self.exp = self.chain.evt.info.exp
        self.evtn = self.chain.evt.info.evtn
        self.data = np.empty(self.chain.GetEntries(), dtype=[
            ('exp', np.int32),
            ('evtn', np.int32),
            ('ds+', np.int32),
            ('ds-', np.int32),
            ('dsj+', np.int32),
            ('dsj-', np.int32),
            ])
        self.run()
        
        # self.vars['tmode'] = self.findDecay(ids['Dsj0+'], 'Dsj') - self.findDecay(ids['Dsj0-'], 'Dsj')\
            #    + 100*self.findDecay(ids['Dsj1+'], 'Dsj') - 100*self.findDecay(ids['Dsj1-'], 'Dsj')
        # self.vars['tdsmode'] = self.findDecay(ids['Ds+'], 'Ds') - self.findDecay(ids['Ds-'], 'Ds')

    def run(self):
        """ Event loop """
        for idx, _ in enumerate(self.chain):
            if idx % 10000 == 0:
                print('{} events'.format(idx))
            dsjp = self.findDecay(ids['Dsj0+'], 'Dsj+')
            if dsjp == -1:
                dsjp = self.findDecay(ids['Dsj1+'], 'Dsj+')
                if dsjp >= 0:
                    dsjp = dsjp * 10**4
            dsjn = self.findDecay(ids['Dsj0-'], 'Dsj-')
            if dsjn == -1:
                dsjn = self.findDecay(ids['Dsj1-'], 'Dsj-')
                if dsjn >= 0:
                    dsjn = dsjn * 10**4
            self.data[idx] = (self.exp, self.evtn,
                self.findDecay(ids['Ds+'], 'Ds+'),
                self.findDecay(ids['Ds-'], 'Ds-'),
                dsjp, dsjn)

    def findDecay(self, idhep, key):
        """ Identify mode in the EvtGen table """
        nphep = np.array(self.idhep)
        idxList = np.nonzero(nphep == idhep)
        if len(idxList[0]) == 0:
            return -1
        idx = idxList[0][0]
        fsp = set([self.idhep[i] for i in np.arange(self.daF[idx], self.daL[idx]+1)])
        for mode, fsps in modesDict[key].iteritems():
            print('{} vs. {}'.format(fsp, fsps))
            if fsp == fsps:
                return mode
        return -1

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
