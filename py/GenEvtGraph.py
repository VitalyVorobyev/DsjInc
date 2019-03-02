""" Tool to make graph decay """

import numpy as np

from pdgcode import ids_stable

class GenEvtGraph(object):
    """ """
    def __init__(self, idhep, daf, dal):
        """ Constructor """
        self.id = np.array(idhep)
        self.df = np.array(daf)
        self.dl = np.array(dal)

    def findDecays(self, idhep):
        """ Find all decays of particles with 'id' """
        idxList = np.nonzero(self.id == idhep)
        if not idxList:
            return None
        decays = []
        for idx in idxList:
            decays.append([self.id[i] for i in np.arange(self.df[i], self.dl[i])])
        return decays

    def getFSP(self, idx, fsp=None):
        """ Collect final-state-particles """
        if fsp is None:
            fsp = []
        for i in range(self.df[i] - 1, self.dl[i]):
            if i >= len(self.id):  # out of recorded particles
                continue
            if self.id[i] in ids_stable:  # add stable particle
                fsp.append(self.id[i])
            else:  # iterative search for unstable particle
                fsp = self.getFSP(i, fsp)
        return fsp
