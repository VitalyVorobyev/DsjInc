""" Exploratory data analysis for signal MC """

__author__ = 'Vitaly Vorobyev'
__date__ = 'January 2019'

from os import listdir
from os.path import isfile, join
from glob import glob

from ROOT import TFile, TCanvas, gSystem, TBrowser

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from lvect import Vect, LVect

tuplePath   = '/home/vitaly/work/DsjInc/tuples'

def sigMCFile(ty, st):
    """ Get root file name """
    pattern = '/'.join([tuplePath, 'signt', '_'.join(['dsjinc', 'sigmc', 'ty' + ty, 'st' + str(st), '*.root'])])
    # print(pattern)
    return glob(pattern)

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

def main():
    """ Unit test """
    # gSystem.Load('libRecoObj.so')
    gSystem.Load('libdsjdata.so')

    # print(sigMCFile('ds', 1))
    print(sigMCFile('dsst0', 1))
    # print(sigMCFile('dsst1', 1))
    # print(sigMCFile('dsUps', 0))

    dst, dsstt, f = getTree(sigMCFile('dsst0', 1)[0])
    dsstt.Draw('m', 'dsj_gen.flag == 1')

    # b = TBrowser()
    # c = TCanvas('c', 'c')
    raw_input()

if __name__ == '__main__':
    main()
