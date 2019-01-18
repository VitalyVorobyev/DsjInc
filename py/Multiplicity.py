""" Calculation of the candidates multiplicity """

import numpy as np
from ROOT import gSystem, TChain

class MultCalc(object):
    """ """
    def __init__(self, data, mode):
        """ Constructor """
        self.data = data

    def run(self):
        """ """
        print('{} events'.format(self.data.GetEntries()))
        mu = np.zeros(100000, dtype='float')
        cnt, cevtn, sigflag = 0, -1, False
        # evt = self.data.evt
        # mcevt = self.data.mcevt
        for evt in self.data:
            if evt.evt.info.evtn == cevtn:
                cnt = cnt + 1
                sigflag = sigflag or (evt.mcevt.dsj_gen.flag in [1, 5, 10])
            else:
                if sigflag:
                    # print(cnt)
                    mu[cnt] = mu[cnt] + 1
                    sigflag = False
                cevtn = evt.evt.info.evtn
                cnt = 1
        mu[cnt] = mu[cnt] + 1
        return mu / mu.sum()

def main():
    """ Unit test """
    gSystem.Load('libRecoObj.so')
    gSystem.Load('libdsjdata.so')
    dsj = TChain('dsj_0', 'dsj_0')
    # dsj.Add('/home/vitaly/work/DsjInc/tuples/signt/dsjinc_sigmc_tydsst1_st1_ex55.root')
    dsj.Add('/home/vitaly/work/DsjInc/tuples/signt/dsjinc_sigmc_dsst1_st1_split.root')
    # print(dsj.Show(0))
    print(dsj.GetEntries())

    mc = MultCalc(dsj, 0)
    mult = mc.run()
    for idx, val in enumerate(mult[:100]):
        print('{:02d} : {:04f}'.format(idx, val))

if __name__ == '__main__':
    main()
