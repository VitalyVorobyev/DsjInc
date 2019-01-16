#! /usr/bin/python2

""" Plotting routines """

from vars import fitRange

from ROOT.RooFit import MarkerSize, Components, LineStyle
from ROOT.RooFit import LineWidth, Title, DataError
from ROOT import RooAbsData
from ROOT import TCanvas, TPad, TLine, kBlue, kDashed

def makePlot(mds, ds, pdf):
    """ Mass fit plot """
    frame = mds.frame()
    ds.plotOn(frame, DataError(RooAbsData.SumW2), MarkerSize(1))
    pdf.plotOn(frame, LineWidth(2))

    # pull histogram
    pullHist = frame.pullHist()
    pullFrame = mds.frame(Title(''))
    pullFrame.addPlotable(pullHist, 'P')
    pullFrame.GetYaxis().SetRangeUser(-5, 5)

    canvas = TCanvas('m(Ds)', 'm(Ds)', 600, 700)
    canvas.cd()

    pad1 = TPad('pad1', 'pad1', .01, .20, .99, .99)
    pad2 = TPad('pad2', 'pad2', .01, .01, .99, .20)
    pad1.Draw()
    pad2.Draw()

    pad1.cd()
    pad1.SetLeftMargin(0.15)
    pad1.SetFillColor(0)

    frame.GetXaxis().SetTitleSize(0.05)
    frame.GetXaxis().SetTitleOffset(0.85)
    frame.GetXaxis().SetLabelSize(0.04)
    frame.GetYaxis().SetTitleOffset(1.6)
    frame.Draw()

    pad2.cd()
    pad2.SetLeftMargin(0.15)
    pad2.SetFillColor(0)
    
    pullFrame.SetMarkerSize(0.05)
    pullFrame.Draw()

    mdsRange = fitRange()['mDs']
    lineUp = TLine(mdsRange[0], 3, mdsRange[1], 3)
    lineUp.SetLineColor(kBlue)
    lineUp.SetLineStyle(2)
    lineUp.Draw()

    lineCe = TLine(mdsRange[0], 0, mdsRange[1], 0)
    lineCe.SetLineColor(kBlue)
    lineCe.SetLineStyle(1)
    lineCe.SetLineWidth(2)
    lineCe.Draw()

    lineD0 = TLine(mdsRange[0], -3, mdsRange[0], -3)
    lineD0.SetLineColor(kBlue)
    lineD0.SetLineStyle(2)
    lineD0.Draw()

    canvas.Update()