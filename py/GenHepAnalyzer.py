""" """

from glob import glob
import numpy as np

from ROOT import TChain, gSystem

from pdgcode import ids, names
from GenEvtGraph import GenEvtGraph

tuplePath = '/home/vitaly/work/DsjInc/tuples'

def sigMCFile(ty, st):
    """ Get root file name """
    return glob('/'.join([tuplePath, 'signt', '_'.join(['dsjinc', 'sigmc', 'ty' + ty, 'st' + str(st), '*.root'])]))

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

    def get(self, key):
        """ """
        assert(key in self._get)
        return self._get[key]()

    def run(self):
        """ Event loop """
        self.ddata = {key: [] for key in ['exp', 'evtn', 'id', 'mode']}
        curEvt = (-1, -1)
        for idx, _ in enumerate(self.chain):
            if idx % 1000 == 0:
                print('{} events'.format(idx))
            if (self.get('exp'), self.get('evtn')) == curEvt:
                continue
            else:
                curEvt = (self.get('exp'), self.get('evtn'))
            gr = GenEvtGraph(self.get('idhep'), self.get('daF'), self.get('daL'))
            for key in ['Ds+', 'Ds-', 'Dsj0+', 'Dsj0-', 'Dsj1+', 'Dsj0-']:
                decs = gr.findDecays(ids[key])
                if decs is None:
                    continue
                for _, h in decs:
                    self.ddata['exp'].append(curEvt[0])
                    self.ddata['evtn'].append(curEvt[1])
                    self.ddata['id'].append(ids[key])
                    self.ddata['mode'].append(h)
        
        self.data = np.empty(len(self.ddata['exp']),
                    dtype=[('exp', np.int32), ('evtn', np.int32), ('id', np.int32), ('mode', np.int32)])
        for key, val in self.ddata.iteritems():
            self.data[key] = val
        return self.data

def main():
    """ Unit test """
    # print(modesDict)
    gSystem.Load('libRecoObj.so')
    gSystem.Load('libdsjdata.so')
    chain = TChain('ds', 'ds')
    key, stream = 'dsst0Neg', 0
    for fname in sigMCFile(key, stream):
        print(fname)
        chain.Add(fname)
    print('{} Ds candidates'.format(chain.GetEntries()))
    gha = GenHepAnalyser(chain)
    data = gha.run()
    print(data[:10])
    truthPath = '/home/vitaly/work/DsjInc/tuples/signt/truth'
    np.save('/'.join([truthPath, 'mctruth_{}_{}.npy'.format(key, stream)]), data)

    print('Hash table:')
    for h, fsp in GenEvtGraph.hashTbl.iteritems():
        print(' {}: {}'.format(h, [names[idhep] for idhep in fsp]))

if __name__ == '__main__':
    main()
