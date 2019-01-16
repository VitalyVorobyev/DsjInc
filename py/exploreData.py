#! /usr/bin/python2

""" Example code """

from os import listdir
from os.path import isfile, join

from ROOT import TFile, TCanvas, gSystem

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from lvect import Vect, LVect

mDs = 1.969
mDssq = mDs**2

tuplePath   = '/home/vitaly/Documents/Students/Kristina/DsJ/tuples'
files = {
    'crm' : 'dsjinc_e7_rs0_re1497_str10_charm.root',
    'mix' : 'dsjinc_e7_rs0_re1497_str10_mixed.root',
    'crg' : 'dsjinc_e7_rs0_re1497_str10_charged.root',
    'uds' : 'dsjinc_e7_rs0_re1497_str10_uds.root'
}

def getTree(fname):
    """ Get TTree from file """
    print(fname)
    f = TFile(fname)
    dstree = f.Get('ds')
    dsjtree = f.Get('dsj')
    print('File {} loaded'.format(fname))
    print(' {} events in Ds tree'.format(dstree.GetEntries()))
    print(' {} events in Dsj tree'.format(dsjtree.GetEntries()))
    return (dstree, dsjtree, f)

def momDs(evt):
    """ Ds momentum """
    pDs = Vect(*np.sum([list(evt.h_ds.p), list(evt.pvec if evt.mode < 2 else evt.ks_ds.p)], axis=0))
    boost = Vect(*list(evt.ipbst.boost))
    pDsCMS = abs(LVect(np.sqrt(mDssq + pDs.abs2()), pDs).boost(boost).r)
    return (abs(pDs), pDsCMS)

def isGoodEvt(ev):
    """ Selection criteria """
    if abs(ev.m - mDs) > 0.012:
        return False
    if ev.mode == 0 and abs(ev.mvec - 1.02) > 0.008:
        return False
    return True

def treeToPd(dst):
    """ Ds TTree to pandas DataFrame """
    evtn, run, exp, pds, pdsst, mode, mds, mvec, mks, flag = [[] for _ in range(10)]
    dst.GetEvent(0)
    evt, mcevt = dst.evt, dst.mcevt
    info = dst.evt.info
    for idx, ev in enumerate(dst):
        if idx % 10000 == 0:
            print('{} events'.format(idx))
        if not isGoodEvt(evt):
            continue
        exp.append(info.exp)
        run.append(info.run)
        evtn.append(info.evtn)
        p, pst = momDs(evt)
        pds.append(p)
        pdsst.append(pst)
        mode.append(evt.mode)
        mds.append(evt.m)
        mvec.append(evt.mvec)
        mks.append(evt.ks_ds.m)
        flag.append(mcevt.ds_gen.flag)
    return pd.DataFrame(
        {'exp'  : exp,
         'run'  : run,
         'evtn' : evtn,
         'pds'  : pds,
         'pdsst': pdsst,
         'mds'  : mds,
         'mks'  : mks,
         'mvec' : mvec,
         'mode' : mode,
         'flag' : flag
        }
    )

def mult(df):
    """ Ds candidates mult filtered """
    mu = np.zeros(10, dtype='float')
    cnt, cevtn, sigflag = 0, df.evtn[0], False
    for idx, ev in df.iterrows():
        if ev.evtn == cevtn:
            cnt = cnt + 1
            if ev.flag in [1, 5, 10]:
                sigflag = True
        else:
            if sigflag:
                mu[cnt] = mu[cnt] + 1
                sigflag = False
            cevtn = ev.evtn
            cnt = 1
    mu[cnt] = mu[cnt] + 1
    return mu / mu.sum()

def makeHist(num, data, var):
    """ """
    colors = {'crm' : 'tan', 'crg' : 'lime', 'mix' : 'blue', 'uds' : 'red'}
    plt.figure(num=num, figsize=(10, 8))
    for key, df in data.iteritems():
        if key is not 'uds':
            plt.hist(df[(df['flag'] ==  1)][var],
               bins=100, normed=True, fill=True, label=key, color=colors[key],
               histtype='bar', alpha=0.3)
    plt.legend(loc='best')
    plt.grid()
    plt.tight_layout()

def multPlot(num, mu, maxmult=7):
    """ """
    plt.figure(num=num, figsize=(4, 3))
    plt.plot(range(1, maxmult), mu[1:maxmult], linestyle='None', marker='.', color='b', markersize=10)
    plt.grid()
    plt.xticks(range(1, maxmult))

def main():
    """ Unit test """
    gSystem.Load('libReco.so')

    data = {key : getTree(join(tuplePath, f)) for key, f in files.iteritems()}
    dfms = {key : treeToPd(dst[0]) for key, dst in data.iteritems()}

    makeHist(1, dfms, 'pds')
    makeHist(2, dfms, 'pdsst')

    mul = {key : mult(df) for key, df in dfms.iteritems()}
    print(mul['crm'])
    print(mul['crg'])
    print(mul['mix'])
    
    multPlot(3, mul['crm'])
    multPlot(4, mul['crg'])
    multPlot(5, mul['mix'])

    plt.show()

if __name__ == '__main__':
    main()
