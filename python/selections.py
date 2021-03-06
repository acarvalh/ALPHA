#! /usr/bin/env python

selection = {
    "triggerMET" : "(isMC?1:(HLT_PFMETNoMu90_PFMHTNoMu90_IDTight_v||HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v||HLT_PFMETNoMu90_JetIdCleaned_PFMHTNoMu90_IDTight_v||HLT_PFMETNoMu120_JetIdCleaned_PFMHTNoMu120_IDTight_v))",
    "triggerIsoEle" : "(isMC?1:HLT_Ele23_WPLoose_Gsf_v)",
    "triggerIsoMuo" : "(isMC?1:(HLT_IsoMu20_v||HLT_IsoTkMu20_v))",
    "triggerEle" : "(isMC?1:(HLT_Ele105_CaloIdVT_GsfTrkIdT_v || HLT_Ele115_CaloIdVT_GsfTrkIdT_v))",
    "triggerMuo" : "(isMC?1:(HLT_Mu45_eta2p1_v))",
    # Leptons
    "singleEle" : "isWtoEN && Lepton1.pt>135 && Lepton1.isTight && V.dPhi<2 && X.dPhi>2 && MEt.pt>80", #  && nTaus==0
    "singleMuo" : "isWtoMN && Lepton1.pt>55 && Lepton1.isHighPt && Lepton1.trkIso<0.1 && V.dPhi<2 && X.dPhi>2", # && nTaus==0
    "singleIsoLep" : "((isWtoEN && Lepton1.isElectron && Lepton1.isLoose && Lepton2.isMuon && Lepton2.isHighPt) || (isWtoMN && Lepton2.isElectron && Lepton2.isLoose && Lepton1.isMuon && Lepton1.isHighPt))",
    "doubleEle" : "isZtoEE && Lepton1.pt>135 && Lepton2.pt>35 && Lepton1.isLoose && Lepton2.isLoose", # && Lepton1.isHighPt && Lepton2.isHighPt && Lepton1.miniIso<0.1 && Lepton2.miniIso<0.1",
    #"doubleMuo" : "isZtoMM && ((Lepton1.isHighPt && Lepton2.isHighPt) || (Lepton1.isTrackerHighPt && Lepton2.isHighPt) || (Lepton1.isHighPt && Lepton2.isTrackerHighPt)) && Lepton1.pt>55 && Lepton2.pt>20 && Lepton1.trkIso<0.1 && Lepton2.trkIso<0.1",
    "doubleMuo" : "isZtoMM && ((Lepton1.isHighPt && Lepton2.isHighPt) || (Lepton1.isTrackerHighPt && Lepton2.isHighPt) || (Lepton1.isHighPt && Lepton2.isTrackerHighPt)) && Lepton1.pt>55 && Lepton2.pt>20 && abs(Lepton1.eta)<2.1 && abs(Lepton2.eta)<2.1 && !(Lepton1.pt>500 && abs(Lepton1.eta)>1.2) && !(Lepton2.pt>500 && abs(Lepton2.eta)>1.2) && Lepton1.trkIso<0.1 && Lepton2.trkIso<0.1",


    "MuonEle" : "((Lepton1.isMuon && Lepton1.isHighPt && Lepton1.pt>55 && Lepton1.trkIso<0.1 && abs(Lepton1.eta)<2.1 && !(Lepton1.pt>500 && abs(Lepton1.eta)>1.2) && Lepton2.isElectron && Lepton2.pt>35 && Lepton2.isLoose) || (Lepton1.isElectron && Lepton1.pt>35 && Lepton1.isLoose && Lepton2.isMuon && Lepton2.isHighPt && Lepton2.pt>55 && abs(Lepton2.eta)<2.1 && !(Lepton2.pt>500 && abs(Lepton2.eta)>1.2) && Lepton2.trkIso<0.1))", # && Lepton1.isHighPt && Lepton2.isHighPt && Lepton1.miniIso<0.1 && Lepton2.miniIso<0.1",


    "doubleIsoEle" : "isZtoEE && Lepton1.pt>25 && Lepton2.pt>10 && Lepton1.isLoose && Lepton2.isLoose",
    "doubleIsoMuo" : "isZtoMM && ((Lepton1.isHighPt && Lepton2.isHighPt) || (Lepton1.isTrackerHighPt && Lepton2.isHighPt) || (Lepton1.isHighPt && Lepton2.isTrackerHighPt)) && Lepton1.pt>25 && Lepton2.pt>10 && Lepton1.trkIso<0.1 && Lepton2.trkIso<0.1",
    "noLeptons" : "MEt.pt>200 && nMuons==0 && nElectrons==0 && nPhotons==0 && FatJet1.isTight && MinJetMetDPhi>0.5 && X.dPhi>2", #nTaus==0 && 
    # V
#    "Boost" : "V.pt>200 && FatJet1.pt>200",
    "Boost" : "V.pt>170 && FatJet1.pt>170",
    "Zcut" : "V.mass>70 && V.mass<110",
    "Topcut" : "MaxFatJetBTag>0.460",
    "TopVetocut" : "MaxFatJetBTag<0.460",
    "HRcut" : "(FatJet1.softdropPuppiMassCorr>105 && FatJet1.softdropPuppiMassCorr<135)",
    "SBcut" : "((FatJet1.softdropPuppiMassCorr>30 && FatJet1.softdropPuppiMassCorr<65) || (FatJet1.softdropPuppiMassCorr>135))", # && FatJet1.softdropPuppiMassCorr<300
    "SRcut" : "(FatJet1.softdropPuppiMassCorr>65 && FatJet1.softdropPuppiMassCorr<105)",
    "LSBcut" : "FatJet1.softdropPuppiMassCorr>30 && FatJet1.softdropPuppiMassCorr<65",
    "HSBcut" : "FatJet1.softdropPuppiMassCorr>135 && FatJet1.softdropPuppiMassCorr<300",
    "HPcut" : "FatJet1.puppiTau21<0.40",
    "LPcut" : "FatJet1.puppiTau21>0.40 && FatJet1.puppiTau21<0.75",
    "1Btag" : "((FatJet1.CSV1>0.460 && FatJet1.CSV2<0.460) || (FatJet1.CSV1<0.460 && FatJet1.CSV2>0.460))",
    "2Btag" : "(FatJet1.CSV1>0.460 && FatJet1.CSV2>0.460)",
    
    #------------------------------#
    #----------    VZ    ----------#
    #------------------------------#
    "XVZllPre"  : "((triggerEle && doubleEle) || (triggerMuo && doubleMuo)) && Boost && Zcut",
    # 2 electrons
    "XVZeeNoBoost"  : "triggerEle && doubleEle && Zcut",
    "XVZeePre"  : "triggerEle && doubleEle && Boost && Zcut",
    "XVZeeInc"  : "triggerEle && doubleEle && Boost && Zcut && (FatJet1.softdropPuppiMassCorr<65 || FatJet1.softdropPuppiMassCorr>135)",
    #
    "XVZeeSB"  : "triggerEle && doubleEle && Boost && Zcut && SBcut",
    "XVZeeSR"  : "triggerEle && doubleEle && Boost && Zcut && SRcut",
    "XVZeeNR"  : "triggerEle && doubleEle && Boost && Zcut && FatJet1.softdropPuppiMassCorr>30",
    #
    "XVZeelpSB" : "triggerEle && doubleEle && Boost && Zcut && LPcut && SBcut",
    "XVZeehpSB" : "triggerEle && doubleEle && Boost && Zcut && HPcut && SBcut",
    #
    "XVZeelpSR" : "triggerEle && doubleEle && Boost && Zcut && LPcut && SRcut",
    "XVZeehpSR" : "triggerEle && doubleEle && Boost && Zcut && HPcut && SRcut",
    # 2 muons
    "XVZmmNoBoost"  : "triggerMuo && doubleMuo && Zcut",
    "XVZmmPre"  : "triggerMuo && doubleMuo && Boost && Zcut",
    "XVZmmInc"  : "triggerMuo && doubleMuo && Boost && Zcut && (FatJet1.softdropPuppiMassCorr<65 || FatJet1.softdropPuppiMassCorr>135)",
    #
    "XVZmmSB"  : "triggerMuo && doubleMuo && Boost && Zcut && SBcut",
    "XVZmmSR"  : "triggerMuo && doubleMuo && Boost && Zcut && SRcut",
    "XVZmmNR"  : "triggerMuo && doubleMuo && Boost && Zcut && FatJet1.softdropPuppiMassCorr>30",
    #
    "XVZmmlpSB" : "triggerMuo && doubleMuo && Boost && Zcut && LPcut && SBcut",
    "XVZmmhpSB" : "triggerMuo && doubleMuo && Boost && Zcut && HPcut && SBcut",
    #
    "XVZmmlpSR" : "triggerMuo && doubleMuo && Boost && Zcut && LPcut && SRcut",
    "XVZmmhpSR" : "triggerMuo && doubleMuo && Boost && Zcut && HPcut && SRcut",
    # 1 muon 1 electron
    "XVZmeNoBoost"   : "triggerMuo && MuonEle",
    "XVZmelp"   : "triggerMuo && MuonEle && FatJet1.pt>170 && LPcut",
    "XVZmehp"   : "triggerMuo && MuonEle && FatJet1.pt>170 && HPcut",
    "XVZmelpSR" : "triggerMuo && MuonEle && FatJet1.pt>170 && LPcut && SRcut",
    "XVZmehpSR" : "triggerMuo && MuonEle && FatJet1.pt>170 && HPcut && SRcut",
    # 2 leptons (e or m)
    "XVZllNR"  : "(triggerEle && doubleEle && Boost && Zcut && FatJet1.softdropPuppiMassCorr>30) || (triggerMuo && doubleMuo && Boost && Zcut && FatJet1.softdropPuppiMassCorr>30)",
    

    #"XVZmelp"   : "triggerEle && ((Lepton1.isMuon && Lepton1.isHighPt && Lepton1.pt>20 && Lepton1.trkIso<0.1 && Lepton2.isElectron && Lepton2.isLoose && Lepton2.pt>20) || (Lepton2.isMuon && Lepton2.isHighPt && Lepton2.pt>55 && Lepton2.trkIso<0.1 && Lepton1.isElectron && Lepton1.isLoose && Lepton1.pt>20)) && Boost && LPcut && FatJet1.softdropPuppiMassCorr>30",
    #"XVZmehp"   : "triggerEle && ((Lepton1.isMuon && Lepton1.isHighPt && Lepton1.pt>20 && Lepton1.trkIso<0.1 && Lepton2.isElectron && Lepton2.isLoose && Lepton2.pt>20) || (Lepton2.isMuon && Lepton2.isHighPt && Lepton2.pt>55 && Lepton2.trkIso<0.1 && Lepton1.isElectron && Lepton1.isLoose && Lepton1.pt>20)) && Boost && HPcut && FatJet1.softdropPuppiMassCorr>30",

    # 0 leptons
    "XVZnnPre"  : "triggerMET && noLeptons && Boost",
    "XVZnnInc"  : "triggerMET && noLeptons && Boost && TopVetocut && (FatJet1.softdropPuppiMassCorr<65 || FatJet1.softdropPuppiMassCorr>135)",
    #
    "XVZnnlpSB" : "triggerMET && noLeptons && Boost && TopVetocut && LPcut && SBcut",
    "XVZnnhpSB" : "triggerMET && noLeptons && Boost && TopVetocut && HPcut && SBcut",
    #
    "XVZnnlpSR" : "triggerMET && noLeptons && Boost && TopVetocut && LPcut && SRcut",
    "XVZnnhpSR" : "triggerMET && noLeptons && Boost && TopVetocut && HPcut && SRcut",
    # 2 lepton, 1 additional btag
    "XVZlnTR"   : "((triggerEle && singleEle) || (triggerMuo && singleMuo)) && Boost && Topcut",
    "XVZlnlpTR" : "((triggerEle && singleEle) || (triggerMuo && singleMuo)) && Boost && Topcut && LPcut && (SBcut || VRcut || SRcut)",
    "XVZlnhpTR" : "((triggerEle && singleEle) || (triggerMuo && singleMuo)) && Boost && Topcut && HPcut && (SBcut || VRcut || SRcut)",
    # 0 lepton, 1 additional btag
    "XVZnnbTR"  : "triggerMET && noLeptons && Topcut && LPcut && (SBcut || VRcut || SRcut)",
    "XVZnnbbTR" : "triggerMET && noLeptons && Topcut && HPcut && (SBcut || VRcut || SRcut)",
    
    #------------------------------#
    #----------    VH    ----------#
    #------------------------------#
    # 2 electrons
    "XZheePre"  : "triggerEle && doubleEle && Boost && Zcut",
    "XZheeInc"  : "triggerEle && doubleEle && Boost && Zcut && (FatJet1.softdropPuppiMassCorr<65 || FatJet1.softdropPuppiMassCorr>135)",
    #
    "XZheebSB"  : "triggerEle && doubleEle && Boost && Zcut && 1Btag && SBcut",
    "XZheebbSB" : "triggerEle && doubleEle && Boost && Zcut && 2Btag && SBcut",
    #
    "XZheebSR"  : "triggerEle && doubleEle && Boost && Zcut && 1Btag && SRcut",
    "XZheebbSR" : "triggerEle && doubleEle && Boost && Zcut && 2Btag && SRcut",
    # 2 muons
    "XZhmmPre"  : "triggerMuo && doubleMuo && Boost && Zcut",
    "XZhmmInc"  : "triggerMuo && doubleMuo && Boost && Zcut && (FatJet1.softdropPuppiMassCorr<65 || FatJet1.softdropPuppiMassCorr>135)",
    #
    "XZhmmbSB"  : "triggerMuo && doubleMuo && Boost && Zcut && 1Btag && SBcut",
    "XZhmmbbSB" : "triggerMuo && doubleMuo && Boost && Zcut && 2Btag && SBcut",
    #
    "XZhmmbSR"  : "triggerMuo && doubleMuo && Boost && Zcut && 1Btag && SRcut",
    "XZhmmbbSR" : "triggerMuo && doubleMuo && Boost && Zcut && 2Btag && SRcut",
    # 1 electron
    "XWhenPre"  : "triggerEle && singleEle && Boost",
    "XWhenInc"  : "triggerEle && singleEle && Boost && TopVetocut && (FatJet1.softdropPuppiMassCorr<65 || FatJet1.softdropPuppiMassCorr>135)",
    #
    "XWhenbSB"  : "triggerEle && singleEle && Boost && TopVetocut && 1Btag && SBcut",
    "XWhenbbSB" : "triggerEle && singleEle && Boost && TopVetocut && 2Btag && SBcut",
    #
    "XWhenbSR"  : "triggerEle && singleEle && Boost && TopVetocut && 1Btag && SRcut",
    "XWhenbbSR" : "triggerEle && singleEle && Boost && TopVetocut && 2Btag && SRcut",
    # 1 muon
    "XWhmnPre"  : "triggerMuo && singleMuo && Boost",
    "XWhmnInc"  : "triggerMuo && singleMuo && Boost && TopVetocut && (FatJet1.softdropPuppiMassCorr<65 || FatJet1.softdropPuppiMassCorr>135)",
    #
    "XWhmnbSB"  : "triggerMuo && singleMuo && Boost && TopVetocut && 1Btag && SBcut",
    "XWhmnbbSB" : "triggerMuo && singleMuo && Boost && TopVetocut && 2Btag && SBcut",
    #
    "XWhmnbSR"  : "triggerMuo && singleMuo && Boost && TopVetocut && 1Btag && SRcut",
    "XWhmnbbSR" : "triggerMuo && singleMuo && Boost && TopVetocut && 2Btag && SRcut",
    # 0 leptons
    "XZhnnPre"  : "triggerMET && noLeptons && Boost",
    "XZhnnInc"  : "triggerMET && noLeptons && Boost && TopVetocut && (FatJet1.softdropPuppiMassCorr<65 || FatJet1.softdropPuppiMassCorr>135)",
    #
    "XZhnnbSB"  : "triggerMET && noLeptons && Boost && TopVetocut && 1Btag && SBcut",
    "XZhnnbbSB" : "triggerMET && noLeptons && Boost && TopVetocut && 2Btag && SBcut",
    #
    "XZhnnbSR"  : "triggerMET && noLeptons && Boost && TopVetocut && 1Btag && SRcut",
    "XZhnnbbSR" : "triggerMET && noLeptons && Boost && TopVetocut && 2Btag && SRcut",
    # 1 lepton, 1 additional btag
    "XWhlnTR"   : "((triggerEle && singleEle) || (triggerMuo && singleMuo)) && Boost && Topcut",
    "XWhlnbTR"  : "((triggerEle && singleEle) || (triggerMuo && singleMuo)) && Boost && Topcut && 1Btag && (SBcut || VRcut || SRcut)",
    "XWhlnbbTR" : "((triggerEle && singleEle) || (triggerMuo && singleMuo)) && Boost && Topcut && 2Btag && (SBcut || VRcut || SRcut)",
    # 0 lepton, 1 additional btag
    "XZhnnbTR"  : "triggerMET && noLeptons && Boost && Topcut && 1Btag && (SBcut || VRcut || SRcut)",
    "XZhnnbbTR" : "triggerMET && noLeptons && Boost && Topcut && 2Btag && (SBcut || VRcut || SRcut)",
    
    #------------------------------#
    #----------    AZh   ----------#
    #------------------------------#
    "AZheeInc"    : "triggerIsoEle && doubleIsoEle",
    "AZhmmInc"    : "triggerIsoMuo && doubleIsoMuo",
    "AZheejjSB" : "triggerIsoEle && doubleIsoEle && nJets>=2 && V.mass>70 && V.mass<110 && (H.mass<90 || H.mass>140) && Jet1.CSV<0.460 && Jet2.CSV<0.460 && MEt.pt<60",
    "AZhmmjjSB" : "triggerIsoMuo && doubleIsoMuo && nJets>=2 && V.mass>70 && V.mass<110 && (H.mass<90 || H.mass>140) && Jet1.CSV<0.460 && Jet2.CSV<0.460 && MEt.pt<60",
    "AZheebjSB" : "triggerIsoEle && doubleIsoEle && nJets>=2 && V.mass>70 && V.mass<110 && (H.mass<90 || H.mass>140) && ((Jet1.CSV>0.935 && Jet2.CSV<0.460) || (Jet1.CSV<0.460 && Jet2.CSV>0.935)) && MEt.pt<60",
    "AZhmmbjSB" : "triggerIsoMuo && doubleIsoMuo && nJets>=2 && V.mass>70 && V.mass<110 && (H.mass<90 || H.mass>140) && ((Jet1.CSV>0.935 && Jet2.CSV<0.460) || (Jet1.CSV<0.460 && Jet2.CSV>0.935)) && MEt.pt<60",
    "AZheebbSB" : "triggerIsoEle && doubleIsoEle && nJets>=2 && V.mass>70 && V.mass<110 && (H.mass<90 || H.mass>140) && ((Jet1.CSV>0.935 && Jet2.CSV>0.460) || (Jet1.CSV>0.460 && Jet2.CSV>0.935)) && MEt.pt<60",
    "AZhmmbbSB" : "triggerIsoMuo && doubleIsoMuo && nJets>=2 && V.mass>70 && V.mass<110 && (H.mass<90 || H.mass>140) && ((Jet1.CSV>0.935 && Jet2.CSV>0.460) || (Jet1.CSV>0.460 && Jet2.CSV>0.935)) && MEt.pt<60",
    "TopSB" : "triggerIsoMuo && doubleIsoMuo && nJets>=2 && (V.mass<70 || V.mass>110) && MEt.pt>60", #Jet1.CSV>0.935 && Jet2.CSV>0.935 && 
    "AZheebbSR" : "triggerIsoEle && doubleIsoEle && nJets>=2 && V.mass>70 && V.mass<110 && (H.mass>90 && H.mass<140) && ((Jet1.CSV>0.935 && Jet2.CSV>0.460) || (Jet1.CSV>0.460 && Jet2.CSV>0.935)) && MEt.pt<60",
    "AZhmmbbSR" : "triggerIsoMuo && doubleIsoMuo && nJets>=2 && V.mass>70 && V.mass<110 && (H.mass>90 && H.mass<140) && ((Jet1.CSV>0.935 && Jet2.CSV>0.460) || (Jet1.CSV>0.460 && Jet2.CSV>0.935)) && MEt.pt<60",
    "AZhllbbSR": "(AZhmmbbSR) || (AZheebbSR)",


    #------------------------------#
    #----------    DM    ----------#
    #------------------------------#

    'DMbbINCZee' : 'isZtoEE && (isMC?1:HLT_Ele27_WPTight_Gsf_v)             && Lepton1.isElectron && Lepton2.isElectron && ((Lepton1.pt>40 && Lepton1.isTight && Lepton2.pt>20 && Lepton2.isLoose)||(Lepton1.pt>20 && Lepton1.isLoose && Lepton2.pt>40 && Lepton2.isTight)) && V.mass > 70 && V.mass<110',
    'DMbbINCZmm' : 'isZtoMM && (isMC?1:(HLT_IsoMu22_v||HLT_IsoTkMu22_v))    && Lepton1.isMuon && Lepton2.isMuon && ((Lepton1.pt>40 && Lepton1.isTight && Lepton1.pfIso04<0.15 && Lepton2.pt>20 && Lepton2.isLoose && Lepton2.pfIso04<0.25)||(Lepton1.pt>20 && Lepton1.isLoose && Lepton1.pfIso04<0.25 && Lepton2.pt>40 && Lepton2.isTight && Lepton2.pfIso04<0.15)) && V.mass > 70 && V.mass<110',
    'DMbbINCWen' : 'isWtoEN && (isMC?1:HLT_Ele27_WPTight_Gsf_v)             && Lepton1.isElectron && Lepton1.pt>40 && Lepton1.isTight && V.tmass>50',
    'DMbbINCWmn' : 'isWtoMN && (isMC?1:(HLT_IsoMu22_v||HLT_IsoTkMu22_v))    && Lepton1.isMuon && Lepton1.pt>40 && Lepton1.isTight && Lepton1.pfIso04<0.15 && V.tmass>50',
    'DMbbINCTme' : 'isTtoEM && (isMC?1:(HLT_IsoMu22_v||HLT_IsoTkMu22_v))    && Lepton1.isTight && Lepton2.isTight && Lepton1.pt>40 && Lepton2.pt>40 && ((Lepton1.isMuon && Lepton1.pfIso04<0.15 && Lepton2.isElectron)||(Lepton2.isMuon && Lepton2.pfIso04<0.15 && Lepton1.isElectron)) && ((Lepton1.charge>0 && Lepton2.charge<0)||(Lepton2.charge>0 && Lepton1.charge<0))',

    'DMbbCRZee' : 'DMbbINCZee && hadronicRecoil.pt>200 && nElectrons>=2 && nMuons==0 && nTaus==0 && Jet1.pt>50 && MinJetMetDPhi>0.5',
    'DMbbCRZmm' : 'DMbbINCZmm && hadronicRecoil.pt>200 && nElectrons==0 && nMuons>=2 && nTaus==0 && Jet1.pt>50 && MinJetMetDPhi>0.5',
    'DMbbCRWen' : 'DMbbINCWen && hadronicRecoil.pt>200 && nElectrons==1 && nMuons==0 && nTaus==0 && Jet1.pt>50 && MinJetMetDPhi>0.5 && V.tmass>50 && V.tmass<160',
    'DMbbCRWmn' : 'DMbbINCWmn && hadronicRecoil.pt>200 && nElectrons==0 && nMuons==1 && nTaus==0 && Jet1.pt>50 && MinJetMetDPhi>0.5 && V.tmass>50 && V.tmass<160',
    'DMbbCRTme' : 'DMbbINCTme && hadronicRecoil.pt>200 && nElectrons==1 && nMuons==1 && nTaus==0 && Jet1.pt>50 && MinJetMetDPhi>0.5',


    #'DMbbZeeCR' : 'isZtoEE && isZCR && (isMC?1:HLT_Ele27_WPLoose_Gsf_v)             && Lepton1.pt>40',
    #'DMbbZmmCR' : 'isZtoMM && isZCR && (isMC?1:(HLT_IsoMu22_v||HLT_IsoTkMu22_v))    && Lepton1.pt>40',
    #'DMbbWenCR' : 'isWtoEN && isWCR && (isMC?1:HLT_Ele27_WPLoose_Gsf_v)             && Lepton1.pt>40',
    #'DMbbWmnCR' : 'isWtoMN && isWCR && (isMC?1:(HLT_IsoMu22_v||HLT_IsoTkMu22_v))    && Lepton1.pt>40',
    #'DMbbTmeCR' : 'isTtoEM && isTCR && (isMC?1:(HLT_IsoMu22_v||HLT_IsoTkMu22_v))    && Lepton1.pt>40',
    #'DMbbSR'    : 'isZtoNN && isSR  && (isMC?1:(HLT_PFMETNoMu90_PFMHTNoMu90_IDTight_v||HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v||HLT_PFMETNoMu90_JetIdCleaned_PFMHTNoMu90_IDTight_v||HLT_PFMETNoMu120_JetIdCleaned_PFMHTNoMu120_IDTight_v)) && MEt.pt>200',

    #'DMbb_NL_ZeeCR' : 'DMbbZeeCR && nMuons==0',
    #'DMbb_NL_ZmmCR' : 'DMbbZmmCR && nElectrons==0',
    #'DMbb_NL_WenCR' : 'DMbbWenCR && nMuons==0',
    #'DMbb_NL_WmnCR' : 'DMbbWmnCR && nElectrons==0',
    #'DMbb_NL_TmeCR' : 'DMbbTmeCR && nElectrons==1 && nMuons==1',
    #'DMbb_NL_SR'    : 'DMbbSR    && nElectrons==0 && nMuons==0',

    #'DMbb_NTL_ZeeCR' : 'DMbb_NL_ZeeCR && nTaus==0',
    #'DMbb_NTL_ZmmCR' : 'DMbb_NL_ZmmCR && nTaus==0',
    #'DMbb_NTL_WenCR' : 'DMbb_NL_WenCR && nTaus==0',
    #'DMbb_NTL_WmnCR' : 'DMbb_NL_WmnCR && nTaus==0',
    #'DMbb_NTL_TmeCR' : 'DMbb_NL_TmeCR && nTaus==0',
    #'DMbb_NTL_SR'    : 'DMbb_NL_SR    && nTaus==0',

}

