#! /usr/bin/env python

import os, multiprocessing
import copy
import math
from array import array
from ROOT import ROOT, gROOT, gStyle, gRandom, TSystemDirectory
from ROOT import TFile, TChain, TTree, TCut, TH1, TH1F, TH2F, THStack, TGraph, TGraphAsymmErrors
from ROOT import TStyle, TCanvas, TPad
from ROOT import TLegend, TLatex, TText, TLine, TBox

from Analysis.ALPHA.variables import *
from Analysis.ALPHA.samples import samples

gStyle.SetOptStat(0)

    
##################
#    PROJECT     #
##################

def project(var, cut, reg, weight, samplelist, pd, ntupledir):
    # Create dict
    file = {}
    tree = {}
    chain = {}
    hist = {}
    
    ### Create and fill MC histograms ###
    for i, s in enumerate(samplelist):
        if "HIST" in cut: # Histogram written to file
            tmphist = file[ss].Get(var)
        else: # Project from tree
            chain[s] = TChain("ntuple/tree")
            for j, ss in enumerate(samples[s]['files']):
                if not 'data' in s or ('data' in s and ss in pd):
                    #file[ss] = TFile(ntupledir + ss + ".root", "READ")
                    #tree[ss] = file[ss].Get("ntuple/tree")
                    #nevents = file[ss].Get("ntuple/All/a_nEvents").GetBinContent(1)
                    #tree[ss].SetWeight(nevents)
                    chain[s].Add(ntupledir + ss + ".root")
            if variable[var]['nbins']>0: hist[s] = TH1F(s, ";"+variable[var]['title'], variable[var]['nbins'], variable[var]['min'], variable[var]['max']) # Init histogram
            else: hist[s] = TH1F(s, ";"+variable[var]['title'], len(variable[var]['bins'])-1, array('f', variable[var]['bins']))
            hist[s].Sumw2()
            tmpcut = cut
            if not 'data' in s:
                if s.endswith('_0b'): tmpcut += " && nBJets==0"
                elif s.endswith('_1b'): tmpcut += " && nBJets==1"
                elif s.endswith('_2b'): tmpcut += " && nBJets>=2"
                if s.endswith('_0l'): tmpcut += " && genNl==0"
                elif s.endswith('_1l'): tmpcut += " && genNl==1"
                elif s.endswith('_2l'): tmpcut += " && genNl>=2"
            cutstring = "("+weight+")" + ("*("+tmpcut+")" if len(tmpcut)>0 else "")
            chain[s].Project(s, var, cutstring)
            hist[s].SetOption("%s" % chain[s].GetTree().GetEntriesFast())
            hist[s].Scale(samples[s]['weight'] if hist[s].Integral() >= 0 else 0)

        hist[s].SetFillColor(samples[s]['fillcolor'])
        hist[s].SetFillStyle(samples[s]['fillstyle'])
        hist[s].SetLineColor(samples[s]['linecolor'])
        hist[s].SetLineStyle(samples[s]['linestyle'])
    
    return hist


##################
#      DRAW      #
##################

def draw(hist, data, back, sign, snorm=1, lumi=-1, ratio=0, poisson=False, log=False, channel=""):
    # If not present, create BkgSum
    if not 'BkgSum' in hist.keys():
        hist['BkgSum'] = hist['data_obs'].Clone("BkgSum") if 'data_obs' in hist else hist[back[0]].Clone("BkgSum")
        hist['BkgSum'].Reset("MICES")
        for i, s in enumerate(back): hist['BkgSum'].Add(hist[s])
    hist['BkgSum'].SetMarkerStyle(0)
    
    # Set Poisson error bars
    #if len(data) > 0: hist['data_obs'].SetBinErrorOption(1) # doesn't work
    
    # Poisson error bars for data
    if poisson:
        alpha = 1 - 0.6827
        hist['data_obs'].SetBinErrorOption(TH1.kPoisson)
        data_graph = TGraphAsymmErrors(hist['data_obs'].GetNbinsX())
        data_graph.SetMarkerStyle(hist['data_obs'].GetMarkerStyle())
        data_graph.SetMarkerSize(hist['data_obs'].GetMarkerSize())
        res_graph = data_graph.Clone()
        for i in range(hist['data_obs'].GetNbinsX()):
            N = hist['data_obs'].GetBinContent(i+1)
            B = hist['BkgSum'].GetBinContent(i+1)
            L =  0 if N==0 else ROOT.Math.gamma_quantile(alpha/2,N,1.)
            U =  ROOT.Math.gamma_quantile_c(alpha/2,N+1,1)
            data_graph.SetPoint(i, hist['data_obs'].GetXaxis().GetBinCenter(i+1), N if not N==0 else -1.e99)
            data_graph.SetPointError(i, hist['data_obs'].GetXaxis().GetBinWidth(i+1)/2., hist['data_obs'].GetXaxis().GetBinWidth(i+1)/2., N-L, U-N)
            res_graph.SetPoint(i, hist['data_obs'].GetXaxis().GetBinCenter(i+1), N/B if not B==0 and not N==0 else -1.e99)
            res_graph.SetPointError(i, hist['data_obs'].GetXaxis().GetBinWidth(i+1)/2., hist['data_obs'].GetXaxis().GetBinWidth(i+1)/2., (N-L)/B if not B==0 else -1.e99, (U-N)/B if not B==0 else -1.e99)
    
    
    # Create stack
    bkg = THStack("Bkg", ";"+hist['BkgSum'].GetXaxis().GetTitle()+";Events")
    for i, s in enumerate(back): bkg.Add(hist[s])
    
    # Legend
    n = len([x for x in data+back+['BkgSum']+sign if samples[x]['plot']])
    leg = TLegend(0.7, 0.9-0.05*n, 0.95, 0.9)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0) #1001
    leg.SetFillColor(0)
    if len(data) > 0:
        leg.AddEntry(hist[data[0]], samples[data[0]]['label'], "pl")
    for i, s in reversed(list(enumerate(['BkgSum']+back))):
        leg.AddEntry(hist[s], samples[s]['label'], "f")
    for i, s in enumerate(sign):
        if samples[s]['plot']: leg.AddEntry(hist[s], samples[s]['label'].replace("m_{#Chi}=1 GeV", ""), "fl")
    
    
    # --- Display ---
    c1 = TCanvas("c1", hist.values()[0].GetXaxis().GetTitle(), 800, 800 if ratio else 600)
    
    if ratio:
        c1.Divide(1, 2)
        setTopPad(c1.GetPad(1), ratio)
        setBotPad(c1.GetPad(2), ratio)
    c1.cd(1)
    c1.GetPad(bool(ratio)).SetTopMargin(0.06)
    c1.GetPad(bool(ratio)).SetRightMargin(0.05)
    c1.GetPad(bool(ratio)).SetTicks(1, 1)
    if log:
        c1.GetPad(bool(ratio)).SetLogy()
        
    # Draw
    bkg.Draw("HIST") # stack
    hist['BkgSum'].Draw("SAME, E2") # sum of bkg
    if poisson: data_graph.Draw("SAME, PE")
    elif len(data) > 0: hist['data_obs'].Draw("SAME, PE")
    for i, s in enumerate(sign):
        if samples[s]['plot']:
            hist[s].DrawNormalized("SAME, HIST", hist[s].Integral()*snorm) # signals
    
    bkg.GetYaxis().SetTitleOffset(bkg.GetYaxis().GetTitleOffset()*1.075)
    bkg.SetMaximum((2. if log else 1.2)*max(bkg.GetMaximum(), hist['data_obs'].GetBinContent(hist['data_obs'].GetMaximumBin())+hist['data_obs'].GetBinError(hist['data_obs'].GetMaximumBin())))
    bkg.SetMinimum(max(min(hist['BkgSum'].GetBinContent(hist['BkgSum'].GetMinimumBin()), hist['data_obs'].GetMinimum()), 5.e-1)  if log else 0.)
    if log:
        bkg.GetYaxis().SetNoExponent(bkg.GetMaximum() < 1.e4)
        bkg.GetYaxis().SetMoreLogLabels(True)
    
    leg.Draw()
    drawCMS(lumi, "Preliminary")
    #drawRegion(channel)
    #drawAnalysis(channel)
    
    #if nm1 and not cutValue is None: drawCut(cutValue, bkg.GetMinimum(), bkg.GetMaximum()) #FIXME
    if len(sign) > 0:
        if channel.startswith('X') and len(sign)>0: drawNorm(0.9-0.04*(n+1), "#sigma(X) #times B(X #rightarrow Vh) = %.1f pb" % snorm)
        #elif "SR" in channel: drawNorm(0.9-0.04*(n+1), "DM+bb/tt, scaled by %.0f" % snorm, "m_{#chi}=1 GeV, scalar mediator")
        elif "SR" in channel: drawNorm(0.9-0.04*(n+1), "DM+bb/tt, m_{#chi}=1 GeV", "scalar mediator")
    
    setHistStyle(bkg, 1.2 if ratio else 1.1)
    setHistStyle(hist['BkgSum'], 1.2 if ratio else 1.1)
       
    if ratio:
        c1.cd(2)
        err = hist['BkgSum'].Clone("BkgErr;")
        err.SetTitle("")
        err.GetYaxis().SetTitle("Data / Bkg")
        for i in range(1, err.GetNbinsX()+1):
            err.SetBinContent(i, 1)
            if hist['BkgSum'].GetBinContent(i) > 0:
                err.SetBinError(i, hist['BkgSum'].GetBinError(i)/hist['BkgSum'].GetBinContent(i))
        setBotStyle(err)
        errLine = err.Clone("errLine")
        errLine.SetLineWidth(1)
        errLine.SetFillStyle(0)
        res = hist['data_obs'].Clone("Residues")
        for i in range(0, res.GetNbinsX()+1):
            if hist['BkgSum'].GetBinContent(i) > 0: 
                res.SetBinContent(i, res.GetBinContent(i)/hist['BkgSum'].GetBinContent(i))
                res.SetBinError(i, res.GetBinError(i)/hist['BkgSum'].GetBinContent(i))
        setBotStyle(res)
        #err.GetXaxis().SetLabelOffset(err.GetXaxis().GetLabelOffset()*5)
        #err.GetXaxis().SetTitleOffset(err.GetXaxis().GetTitleOffset()*2)
        err.Draw("E2")
        errLine.Draw("SAME, HIST")
        if len(data) > 0:
            #res.Draw("SAME, PE0")
            res_graph.Draw("SAME, PE0")
            if len(err.GetXaxis().GetBinLabel(1))==0: # Bin labels: not a ordinary plot
                drawRatio(hist['data_obs'], hist['BkgSum'])
                drawKolmogorov(hist['data_obs'], hist['BkgSum'])
    
    c1.Update()
    
    # return list of objects created by the draw() function
    return [c1, bkg, leg, err, errLine, res, data_graph, res_graph]

def drawRatio(data, bkg):
    errData = array('d', [1.0])
    errBkg = array('d', [1.0])
    intData = data.IntegralAndError(1, data.GetNbinsX(), errData)
    intBkg = bkg.IntegralAndError(1, bkg.GetNbinsX(), errBkg)
    ratio = intData / intBkg if intBkg!=0 else 0.
    error = math.hypot(errData[0]*ratio/intData,  errBkg[0]*ratio/intBkg) if intData>0 and intBkg>0 else 0
    latex = TLatex()
    latex.SetNDC()
    latex.SetTextColor(1)
    latex.SetTextFont(62)
    latex.SetTextSize(0.08)
    latex.DrawLatex(0.25, 0.85, "Data/Bkg = %.3f #pm %.3f" % (ratio, error))
    print "  Ratio:\t%.3f +- %.3f" % (ratio, error)
    #return [ratio, error]

def drawKolmogorov(data, bkg):
    latex = TLatex()
    latex.SetNDC()
    latex.SetTextColor(1)
    latex.SetTextFont(62)
    latex.SetTextSize(0.08)
    latex.DrawLatex(0.55, 0.85, "#chi^{2}/ndf = %.2f,   K-S = %.3f" % (data.Chi2Test(bkg, "CHI2/NDF"), data.KolmogorovTest(bkg)))

def printTable(hist, sign=[]):
    samples = [x for x in hist.keys() if not 'data' in x and not 'BkgSum' in x and not x in sign]
    print "Sample                  Events          Entries         %"
    print "-"*80
    for i, s in enumerate(['data_obs']+samples+['BkgSum']):
        if i==1 or i==len(samples)+1: print "-"*80
        print "%-20s" % s, "\t%-10.2f" % hist[s].Integral(), "\t%-10.0f" % (hist[s].GetEntries()-2), "\t%-10.2f" % (100.*hist[s].Integral()/hist['BkgSum'].Integral()) if hist['BkgSum'].Integral() > 0 else 0, "%"
    print "-"*80
    for i, s in enumerate(sign):
        if not sample[s]['plot']: continue
        print "%-20s" % s, "\t%-10.2f" % hist[s].Integral(), "\t%-10.0f" % (hist[s].GetEntries()-2), "\t%-10.2f" % (100.*hist[s].GetEntries()/float(hist[s].GetOption())) if float(hist[s].GetOption()) > 0 else 0, "%"    
    print "-"*80

##################
#     OTHERS     #
##################

def getPrimaryDataset(cut):
    pd = []
    if 'HLT_DoubleMu' in cut or cut.split(" ")[0].count('Mu') > 1: pd += [x for x in samples['data_obs']['files'] if "DoubleMuon" in x]
    if 'HLT_DoubleEle' in cut or cut.split(" ")[0].count('Ele') > 1: pd += [x for x in samples['data_obs']['files'] if "DoubleEG" in x]
    if ('HLT_Mu' in cut or 'HLT_IsoMu' in cut): pd += [x for x in samples['data_obs']['files'] if "SingleMuon" in x]
    if 'HLT_Ele' in cut: pd += [x for x in samples['data_obs']['files'] if "SingleElectron" in x]
    if 'HLT_PFMET' in cut: pd += [x for x in samples['data_obs']['files'] if "MET" in x]
    return pd


def addOverflow(hist, addUnder=True):
    n = hist.GetNbinsX()
    hist.SetBinContent(n, hist.GetBinContent(n) + hist.GetBinContent(n+1))
    hist.SetBinError(n, math.sqrt( hist.GetBinError(n)**2 + hist.GetBinError(n+1)**2 ) )
    hist.SetBinContent(n+1, 0.)
    hist.SetBinError(n+1, 0.)
    if addUnder:
        hist.SetBinContent(1, hist.GetBinContent(0) + hist.GetBinContent(1))
        hist.SetBinError(1, math.sqrt( hist.GetBinError(0)**2 + hist.GetBinError(1)**2 ) )
        hist.SetBinContent(0, 0.)
        hist.SetBinError(0, 0.)

def setTopPad(TopPad, r=4):
    TopPad.SetPad("TopPad", "", 0., 1./r, 1.0, 1.0, 0, -1, 0)
    TopPad.SetTopMargin(0.24/r)
    TopPad.SetBottomMargin(0.04/r)
    TopPad.SetRightMargin(0.05)
    TopPad.SetTicks(1, 1)

def setBotPad(BotPad, r=4):
    BotPad.SetPad("BotPad", "", 0., 0., 1.0, 1./r, 0, -1, 0)
    BotPad.SetTopMargin(r/100.)
    BotPad.SetBottomMargin(r/10.)
    BotPad.SetRightMargin(0.05)
    BotPad.SetTicks(1, 1)

def setHistStyle(hist, r=1.1):
    hist.GetXaxis().SetTitleSize(hist.GetXaxis().GetTitleSize()*r*r)
    hist.GetYaxis().SetTitleSize(hist.GetYaxis().GetTitleSize()*r*r)
    hist.GetXaxis().SetLabelSize(hist.GetXaxis().GetLabelSize()*r)
    hist.GetYaxis().SetLabelSize(hist.GetYaxis().GetLabelSize()*r)
    hist.GetXaxis().SetLabelOffset(hist.GetXaxis().GetLabelOffset()*r*r*r*r)
    hist.GetXaxis().SetTitleOffset(hist.GetXaxis().GetTitleOffset()*r)
    hist.GetYaxis().SetTitleOffset(hist.GetYaxis().GetTitleOffset())
    if hist.GetXaxis().GetTitle().find("GeV") != -1: # and not hist.GetXaxis().IsVariableBinSize()
        div = (hist.GetXaxis().GetXmax() - hist.GetXaxis().GetXmin()) / hist.GetXaxis().GetNbins()
        hist.GetYaxis().SetTitle("Events / %.1f GeV" % div)

def setBotStyle(h, r=4, fixRange=True):
    h.GetXaxis().SetLabelSize(h.GetXaxis().GetLabelSize()*(r-1));
    h.GetXaxis().SetLabelOffset(h.GetXaxis().GetLabelOffset()*(r-1));
    h.GetXaxis().SetTitleSize(h.GetXaxis().GetTitleSize()*(r-1));
    h.GetYaxis().SetLabelSize(h.GetYaxis().GetLabelSize()*(r-1));
    h.GetYaxis().SetNdivisions(505);
    h.GetYaxis().SetTitleSize(h.GetYaxis().GetTitleSize()*(r-1));
    h.GetYaxis().SetTitleOffset(h.GetYaxis().GetTitleOffset()/(r-1));
    if fixRange:
        h.GetYaxis().SetRangeUser(0., 2.)
        for i in range(1, h.GetNbinsX()+1):
            if h.GetBinContent(i)<1.e-6:
                h.SetBinContent(i, -1.e-6)

##################
### DRAW UTILS ###
##################

def drawCMS(lumi, text, onTop=False):
    latex = TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.04)
    latex.SetTextColor(1)
    latex.SetTextFont(42)
    latex.SetTextAlign(33)
    if (type(lumi) is float or type(lumi) is int) and float(lumi) > 0: latex.DrawLatex(0.95, 0.985, "%.2f fb^{-1}  (13 TeV)" % (float(lumi)/1000.))
    elif type(lumi) is str: latex.DrawLatex(0.95, 0.985, "%s fb^{-1}  (13 TeV)" % lumi)
    if not onTop: latex.SetTextAlign(11)
    latex.SetTextFont(62)
    latex.SetTextSize(0.05 if len(text)>0 else 0.06)
    if not onTop: latex.DrawLatex(0.15, 0.87 if len(text)>0 else 0.84, "CMS")
    else: latex.DrawLatex(0.20, 0.99, "CMS")
    latex.SetTextSize(0.04)
    latex.SetTextFont(52)
    if not onTop: latex.DrawLatex(0.15, 0.83, text)
    else: latex.DrawLatex(0.40, 0.98, text)
#    latex.SetTextSize(0.04)
#    latex.SetTextFont(62)
#    latex.SetTextAlign(13)
#    latex.DrawLatex(0.45, 0.98, "DM monojet")

def drawAnalysis(s, center=False):
    text = ""
    if "VH" in s or "Vh" in s or s.startswith('X'): text = "X #rightarrow Vh #rightarrow (ll,l#nu,#nu#nu)bb"
    elif "Zh" in s: text = "Z' #rightarrow Zh #rightarrow (ll,#nu#nu)bb"
    elif "Wh" in s: text = "W' #rightarrow Wh #rightarrow l#nu bb"
    elif "DM" in s or "CR" in s: text = "DM + heavy flavour"
    else: return True
    latex = TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.04)
    latex.SetTextFont(42)
    #latex.SetTextAlign(33)
    latex.DrawLatex(0.15 if not center else 0.3, 0.95, text)



