""" Tool to make graph decay """

import numpy as np

from pdgcode import ids_stable

class GenEvtGraph(object):
    """ """
    hashTbl = {}
    def __init__(self, idhep, daf, dal):
        """ Constructor """
        self.id = np.array(idhep)
        self.df = np.array(daf)
        self.dl = np.array(dal)

    def printGenTable(self):
        """ """
        print('Gen table:')
        for idx, (i, f, l) in enumerate(zip(self.id, self.df, self.dl)):
            print('{}. {}: {} {}'.format(idx, i, f, l))

    def findDecays(self, idhep):
        """ Find all decays of particles with 'id' """
        idxList = np.nonzero(self.id == idhep)[0]
        # print('idxList {}'.format(idxList))
        if len(idxList) == 0:
            return None
        decays = []
        for idx in idxList:
            # print('Idhep {}: index {}'.format(idhep, idx))
            fsp = tuple(sorted(self.getFSP(idx)))
            # print('FSP: {}'.format(fsp))
            h = hash(fsp) % 997
            if h not in GenEvtGraph.hashTbl:
                print('New FS: {} <- {}'.format(fsp, h))
                GenEvtGraph.hashTbl[h] = fsp
            decays.append((fsp, h))
        return decays

    def getFSP(self, idx, fsp=None):
        """ Collect final-state-particles """
        if fsp is None:
            fsp = [self.id[idx]]
        # print('df {}, dl {}'.format(self.df[idx] - 1, self.dl[idx]))
        for i in range(self.df[idx] - 1, self.dl[idx]):
            if i >= len(self.id):  # out of recorded particles
                continue
            if self.id[i] in ids_stable:  # add stable particle
                fsp.append(self.id[i])
            else:  # iterative search for unstable particle
                fsp = self.getFSP(i, fsp)
        return fsp
