"""  Belle runs luminocity analyser

       Author: Vitaly Vorobyev (vvorob@inp.nsk.su)
      Created: September 2018
  Last update: November 2018

"""

import os
import numpy as np

class LumiAnalyzer(object):
    """ """
    def __init__(self, path='/home/belle/vitaly/lumi'):
        """ Constructor """
        self.path = path

    def chopExp(self, exp, size):
        """ """
        data = np.loadtxt('/'.join([self.path, 'lumexp' + str(exp) + '.txt']))
        slices = [0]
        lumiint = 0
        for run, lumi in data:
            if lumiint > size:
                slices.append(int(run))
                lumiint = 0
            else:
                lumiint = lumiint + lumi
        slices.append(int(data[-1][0] + 1))
        return slices

    def expList(self):
        """ """
        return sorted([int(f[6:-4]) for f in os.listdir(self.path)])

def main():
    """ Unit test """
    print('Chop with interval 3 fb^-1')
    la = LumiAnalyzer()
    elist = la.expList()
    print(elist)
    nparts = 0
    for exp in elist:
        print('Exp ' + str(exp))
        runs = la.chopExp(exp, 3000)
        nparts = nparts + len(runs) - 1
        print(runs)
    print(str(nparts) + ' parts')

if __name__ == '__main__':
    main()

