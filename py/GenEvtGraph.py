""" Tool to make graph decay """

import numpy as np

class GenEvtGraph(object):
    """ """
    def __init__(self, idhep, daf, dal):
        """ Constructor """
        self.id = np.array(idhep)
        self.df = np.array(daf)
        self.dl = np.array(dal)

    def buildGraph(self):
        """ """

    def findDecays(self, idhep):
        """ Find all decays of particles with 'id' """
        idxList = np.nonzero(self.id == idhep)
        if not idxList:
            return None
        decays = []
        for idx in idxList:
            decays.append([self.id[i] for i in np.arange(self.df[i], self.dl[i])])
        return decays
