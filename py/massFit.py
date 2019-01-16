#! /usr/bin/python2

""" Mass distribution fitters """

import sys
sys.path.append('/home/vitaly/work/B0toD0pipi/Analysis/py/lib')

# pyROOT
from ROOT import gSystem
from ROOT import RooDataSet, RooRealVar, RooArgSet, RooCategory
from ROOT import RooGaussian #, RooCBShape
from ROOT.RooFit import Verbose, Timer
from ROOT import TFile

# My analysis lib
from RooVarTools import argset, varDict, fitVarDict

# This analysis
from exploreData import getTree, tupleList, tuplePath
from selections import DsPhiPiSelections
from vars import DsPhiPiParams, DsPhiPiFitParams
from plots import makePlot

def massDsSignalPDF(pars, fitPars):
    """ """
    pdf = RooGaussian('pdf', 'pdf', pars['m'], fitPars['mDsMean'], fitPars['mDsWidth'])
    return pdf

def makeDataSet(name, tree, pars, cuts):
    """ Make data set """
    # pars.Print()
    # tree.Draw("m", "")
    return RooDataSet(name, name, tree, pars)

def main():
    """ Unit test """
    # get tuples list
    tuplist = tupleList('genmc', 7)
    # get TTree
    dst, dsjt, f = getTree('/'.join([tuplePath(), tuplist[-1]]))
    
    # get analysis cuts (selections string)
    cuts = DsPhiPiSelections()

    # parameters
    parDict = DsPhiPiParams()
    # fit parameters
    fitParDict = DsPhiPiFitParams()

    # parameters RooArgSet
    vdict = varDict(parDict)
    pars = argset(vdict)
    # fir parameters RooArgSet
    fdict = fitVarDict(fitParDict)
    fitPars = argset(fdict)

    print(cuts)
    ds = makeDataSet('ds', dst, pars, cuts)
    pdf = massDsSignalPDF(pars, fitPars)

    pdf.fitTo(ds, Verbose(), Timer(True))
    makePlot(pars['m'], ds, pdf)
    
    raw_input("Press Enter to continue...")

def main1():
    m = RooRealVar('evt.m', 'evt.m', 1.92, 2.02)
    mode = RooCategory('evt.mode', 'evt.mode')
    mode.defineType('phipi', 0)
    aset = RooArgSet('aset')
    aset.add(m)
    aset.add(mode)

    tuplist = tupleList('genmc', 7)
    dst, _, f = getTree('/'.join([tuplePath(), tuplist[-1]]))
    # dst.Print()
    # dst.Show(0)

    # for evt in dst:
        # print('Hello!')
        # print(evt.evt.m)
        # break

    ds = RooDataSet('ds', 'ds', dst, aset)
    print(ds.numEntries())
    
    mean = RooRealVar('mean', 'mean', 1.96, 1.92, 2.0)
    width = RooRealVar('width', 'width', 0.006, 0.001, 0.010)
    pdf = RooGaussian('pdf', 'pdf', m, mean, width)

    pdf.fitTo(ds, Verbose(), Timer(True))
    makePlot(m, ds, pdf)
    
    raw_input("Press Enter to continue...")

if __name__ == '__main__':
    gSystem.Load('libReco.so')
    main1()
