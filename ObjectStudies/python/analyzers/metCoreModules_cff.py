##########################################################
##          MET COMMON MODULES ARE DEFINED HERE        ##
##########################################################

import PhysicsTools.HeppyCore.framework.config as cfg

from PhysicsTools.Heppy.analyzers.core.all import *
from PhysicsTools.Heppy.analyzers.objects.all import *
from PhysicsTools.Heppy.analyzers.gen.all import *
import os

##------------------------------------------
##  Core modules
##------------------------------------------

from CMGTools.TTHAnalysis.analyzers.ttHhistoCounterAnalyzer import ttHhistoCounterAnalyzer
susyCounter = cfg.Analyzer(
    ttHhistoCounterAnalyzer, name="ttHhistoCounterAnalyzer",
    )

skimAnalyzer = cfg.Analyzer(
    SkimAnalyzerCount, name='skimAnalyzerCount',
    useLumiBlocks = False,
    )

# Pick individual events (normally not in the path)
eventSelector = cfg.Analyzer(
    EventSelector,name="EventSelector",
    toSelect = []  # here put the event numbers (actual event numbers from CMSSW)
    )

PDFWeights = []

# Apply json file (if the dataset has one)
jsonAna = cfg.Analyzer(
    JSONAnalyzer, name="JSONAnalyzer",
    )

# Filter using the 'triggers' and 'vetoTriggers' specified in the dataset
triggerAna = cfg.Analyzer(
    TriggerBitFilter, name="TriggerBitFilter",
    )

# Create flags for trigger bits
triggerFlagsAna = cfg.Analyzer(
    TriggerBitAnalyzer, name="TriggerFlags",
    processName = 'HLT',
    triggerBits = {
        # "<name>" : [ 'HLT_<Something>_v*', 'HLT_<SomethingElse>_v*' ] 
    }
    )

from CMGTools.TTHAnalysis.analyzers.badChargedHadronAnalyzer import badChargedHadronAnalyzer
badChargedHadronAna = cfg.Analyzer(
    badChargedHadronAnalyzer, name = 'badChargedHadronAna',
    muons='slimmedMuons',
    packedCandidates = 'packedPFCandidates',
)

from CMGTools.TTHAnalysis.analyzers.badMuonAnalyzer import badMuonAnalyzer
badMuonAna = cfg.Analyzer(
    badMuonAnalyzer, name = 'badMuonAna',
    muons='slimmedMuons',
    packedCandidates = 'packedPFCandidates',
)

from CMGTools.TTHAnalysis.analyzers.badMuonAnalyzerMoriond2017 import badMuonAnalyzerMoriond2017
badCloneMuonAnaMoriond2017 = cfg.Analyzer(
    badMuonAnalyzerMoriond2017, name = 'badCloneMuonMoriond2017',
    muons = 'slimmedMuons',
    vertices         = 'offlineSlimmedPrimaryVertices',
    minMuPt = 20,
    selectClones = True,
    postFix = '',
)

badMuonAnaMoriond2017 = cfg.Analyzer(
    badMuonAnalyzerMoriond2017, name = 'badMuonMoriond2017',
    muons = 'slimmedMuons',
    vertices         = 'offlineSlimmedPrimaryVertices',
    minMuPt = 20,
    selectClones = False,
    postFix = '',
)

# Create flags for MET filter bits
eventFlagsAna = cfg.Analyzer(
    TriggerBitAnalyzer, name="EventFlags",
    processName = 'PAT',
    outprefix   = 'Flag',
    triggerBits = {
        "goodVertices" : [ "Flag_goodVertices" ],
        "HBHENoiseFilter" : [ "Flag_HBHENoiseFilter" ],
        "HBHENoiseIsoFilter" : [ "Flag_HBHENoiseIsoFilter" ],
        "CSCTightHaloFilter" : [ "Flag_CSCTightHaloFilter" ],
        "CSCTightHalo2015Filter" : [ "Flag_CSCTightHalo2015Filter" ],
        "globalTightHalo2016Filter" : [ "Flag_globalTightHalo2016Filter" ],
        "eeBadScFilter" : [ "Flag_eeBadScFilter" ],
        "EcalDeadCellTriggerPrimitiveFilter" : [ "Flag_EcalDeadCellTriggerPrimitiveFilter" ],
        "badMuons" : [ "Flag_badMuons" ],
        "duplicateMuons" : [ "Flag_duplicateMuons" ],
        "noBadMuons" : [ "Flag_noBadMuons" ],
    }
    )


#from CMGTools.TTHAnalysis.analyzers.hbheAnalyzer import hbheAnalyzer
#hbheFilterAna = cfg.Analyzer(
#    hbheAnalyzer, name = 'hbheAnalyzer',
#    IgnoreTS4TS5ifJetInLowBVRegion = False
#)

# Select a list of good primary vertices (generic)
vertexAna = cfg.Analyzer(
    VertexAnalyzer, name="VertexAnalyzer",
    vertexWeight = None,
    fixedWeight = 1,
    verbose = False
    )


# This analyzer actually does the pile-up reweighting (generic)
pileUpAna = cfg.Analyzer(
    PileUpAnalyzer, name="PileUpAnalyzer",
    true = True,  # use number of true interactions for reweighting
    makeHists=False
    )

##------------------------------------------
##  gen
##------------------------------------------

## Gen Info Analyzer (generic, but should be revised)
genAna = cfg.Analyzer(
    GeneratorAnalyzer, name="GeneratorAnalyzer",
    # BSM particles that can appear with status <= 2 and should be kept
    stableBSMParticleIds = [ 1000022 ],
    # Particles of which we want to save the pre-FSR momentum (a la status 3).
    # Note that for quarks and gluons the post-FSR doesn't make sense,
    # so those should always be in the list
    savePreFSRParticleIds = [ 1,2,3,4,5, 11,12,13,14,15,16, 21 ],
    # Make also the list of all genParticles, for other analyzers to handle
    makeAllGenParticles = True,
    # Make also the splitted lists
    makeSplittedGenLists = True,
    allGenTaus = False,
    # Print out debug information
    verbose = False,
    )

lheWeightAna = cfg.Analyzer(
    LHEWeightAnalyzer, name="LHEWeightAnalyzer",
    useLumiInfo=False
)


## Gen Info Analyzer
from CMGTools.TTHAnalysis.analyzers.ttHGenBinningAnalyzer import ttHGenBinningAnalyzer
ttHGenBinAna = cfg.Analyzer(
    ttHGenBinningAnalyzer, name = 'ttHGenBinningAnalyzer'
    )

##------------------------------------------
##  leptons 
##------------------------------------------

# Lepton Analyzer (generic)
lepAna = cfg.Analyzer(
    LeptonAnalyzer, name="leptonAnalyzer",
    # input collections
    muons='slimmedMuons',
    electrons='slimmedElectrons',
    rhoMuon= 'fixedGridRhoFastjetCentralNeutral',
    rhoElectron = 'fixedGridRhoFastjetCentralNeutral',
    # energy scale corrections and ghost muon suppression (off by default)
    doMuonScaleCorrections=False,
    doElectronScaleCorrections=False,
#    doElectronScaleCorrections = {
#        'data' : 'EgammaAnalysis/ElectronTools/data/ScalesSmearings/80X_Golden22June_approval',
#        'GBRForest': ('$CMSSW_BASE/src/CMGTools/RootTools/data/egamma_epComb_GBRForest_76X.root',
#                      'gedelectron_p4combination_25ns'),
#        'isSync': False
#        },
    doSegmentBasedMuonCleaning=False,
    # inclusive very loose muon selection
    inclusive_muon_id  = "POG_ID_Loose",
    inclusive_muon_pt  = 10,
    inclusive_muon_eta = 2.4,
    inclusive_muon_dxy = 0.5,
    inclusive_muon_dz  = 1.0,
    # loose muon selection
    loose_muon_id     = "POG_ID_Loose",
    loose_muon_pt     = 10,
    loose_muon_eta    = 2.4,
    loose_muon_dxy    = 0.05,
    loose_muon_dz     = 0.1,
    loose_muon_relIso = 0.5,
    muon_dxydz_track = "innerTrack",
    # inclusive very loose electron selection
    inclusive_electron_id  = "POG_Cuts_ID_SPRING16_25ns_v1_ConvVetoDxyDz_Loose",
    inclusive_electron_pt  = 10,
    inclusive_electron_eta = 2.5,
    inclusive_electron_dxy = 0.5,
    inclusive_electron_dz  = 1.0,
    inclusive_electron_lostHits = 1.0,
    # loose electron selection
    loose_electron_id     = "POG_Cuts_ID_SPRING16_25ns_v1_ConvVetoDxyDz_Loose",
    loose_electron_pt     = 10,
    loose_electron_eta    = 2.4,
    loose_electron_dxy    = 0.05,
    loose_electron_dz     = 0.1,
    loose_electron_relIso = 0.5,
    loose_electron_lostHits = 1.0,
    # muon isolation correction method (can be "rhoArea" or "deltaBeta")
    mu_isoCorr = "deltaBeta" ,
    mu_effectiveAreas = "Spring15_25ns_v1", #(can be 'Data2012' or 'Phys14_25ns_v1')
    # electron isolation correction method (can be "rhoArea" or "deltaBeta")
    ele_isoCorr = "deltaBeta" ,
    ele_effectiveAreas = "Spring16_25ns_v1" , #(can be 'Data2012' or 'Phys14_25ns_v1')
    ele_tightId = "Cuts_SPRING16_25ns_v1_ConvVetoDxyDz" ,
    # Mini-isolation, with pT dependent cone: will fill in the miniRelIso, miniRelIsoCharged, miniRelIsoNeutral variables of the leptons (see https://indico.cern.ch/event/368826/ )
    doMiniIsolation = False, # off by default since it requires access to all PFCandidates 
    packedCandidates = 'packedPFCandidates',
    miniIsolationPUCorr = 'deltaBeta', # Allowed options: 'rhoArea' (EAs for 03 cone scaled by R^2), 'deltaBeta', 'raw' (uncorrected), 'weights' (delta beta weights; not validated)
    miniIsolationVetoLeptons = None, # use 'inclusive' to veto inclusive leptons and their footprint in all isolation cones
    # minimum deltaR between a loose electron and a loose muon (on overlaps, discard the electron)
    min_dr_electron_muon = 0.02,
    # do MC matching 
    do_mc_match = False, # note: it will in any case try it only on MC, not on data
    match_inclusiveLeptons = False, # match to all inclusive leptons
    do_mc_match_photons = False, # do not do MC matching of electrons to photons
    )

## Lepton-based Skim (generic, but requirements depend on the final state)
from CMGTools.TTHAnalysis.analyzers.ttHLepSkimmer import ttHLepSkimmer
ttHLepSkim = cfg.Analyzer(
    ttHLepSkimmer, name='ttHLepSkimmer',
    minLeptons = 0,
    maxLeptons = 999,
    #idCut  = "lepton.relIso03 < 0.2" # can give a cut
    #ptCuts = [20,10],                # can give a set of pt cuts on the leptons
    )

## Photon Analyzer (generic)
photonAna = cfg.Analyzer(
    PhotonAnalyzer, name='photonAnalyzer',
    photons='slimmedPhotons',
    doPhotonScaleCorrections=False,
#    doPhotonScaleCorrections = {
#        'data' : 'EgammaAnalysis/ElectronTools/data/ScalesSmearings/80X_Golden22June_approval',
#        'isSync': False
#        },
    ptMin = 30,
    etaMax = 2.5,
    gammaID = "POG_SPRING15_25ns_Tight",
    rhoPhoton = 'fixedGridRhoFastjetAll',
    gamma_isoCorr = 'rhoArea',
    doFootprintRemovedIsolation = True,
    conversionSafe_eleVeto = True,
    do_mc_match = False,
    do_randomCone = False,
    packedCandidates = 'packedPFCandidates',
    footprintRemovedIsolationPUCorr = 'rhoArea',
    )


##------------------------------------------
##  MET
##------------------------------------------

metAna = cfg.Analyzer(
    METAnalyzer, name="metAnalyzer",
    metCollection     = ("slimmedMETs","","RERUN"),
    noPUMetCollection = ("slimmedMETs","","RERUN"),
    copyMETsByValue = False,
    doTkMet = True,
    includeTkMetCHS = True,
    includeTkMetPVLoose = False,
    includeTkMetPVTight = False,
    doMetNoPU = False,
    doMetNoMu = False,
    doMetNoEle = False,
    storePuppiExtra = False,
    doMetNoPhoton = False,
    recalibrate = False, # or "type1", or True or False if pre-processor is used
    applyJetSmearing = False, # does nothing unless the jet smearing is turned on in the jet analyzer
    old74XMiniAODs = False, # set to True to get the correct Raw MET when running on old 74X MiniAODs
    jetAnalyzerPostFix = "",
    candidates='packedPFCandidates',
    candidatesTypes='std::vector<pat::PackedCandidate>',
    dzMax = 0.1,
    collectionPostFix = "",
    )

metAnaScaleUp = metAna.clone(name="metAnalyzerScaleUp",
    copyMETsByValue = True,
    recalibrate = "type1",
    jetAnalyzerPostFix = "_jecUp",
    collectionPostFix = "_jecUp",
    )

metAnaScaleDown = metAna.clone(name="metAnalyzerScaleDown",
    copyMETsByValue = True,
    recalibrate = "type1",
    jetAnalyzerPostFix = "_jecDown",
    collectionPostFix = "_jecDown",
    )


metPuppiAna = cfg.Analyzer(
    METAnalyzer, name="metAnalyzerPuppi",
    metCollection     = ("slimmedMETsPuppi","","RERUN"),
    noPUMetCollection = ("slimmedMETsPuppi","","RERUN"),
    copyMETsByValue = False,
    doTkMet = False,
    includeTkMetCHS = False,
    includeTkMetPVLoose = False,
    includeTkMetPVTight = False,
    doMetNoPU = False,
    doMetNoMu = False,
    doMetNoEle = False,
    doMetNoPhoton = False,
    storePuppiExtra = False, # False for MC, True for re-MiniAOD
##    recalibrate = "type1", # or "type1", or True
    recalibrate = False, # or "type1", or True or False if pre-processor is used
    applyJetSmearing = False, # does nothing unless the jet smearing is turned on in the jet analyzer
    old74XMiniAODs = False, # set to True to get the correct Raw MET when running on old 74X MiniAODs
    jetAnalyzerPostFix = "Puppi",
    candidates='packedPFCandidates',
    candidatesTypes='std::vector<pat::PackedCandidate>',
    dzMax = 0.1,
    collectionPostFix = "Puppi",
    )

metPuppiAnaScaleUp = metPuppiAna.clone(name="metAnalyzerPuppiScaleUp",
    copyMETsByValue = True,
    recalibrate = "type1",
    jetAnalyzerPostFix = "Puppi_jecUp",
    collectionPostFix = "Puppi_jecUp",
    )

metPuppiAnaScaleDown = metPuppiAna.clone(name="metAnalyzerPuppiScaleDown",
    copyMETsByValue = True,
    recalibrate = "type1",
    jetAnalyzerPostFix = "Puppi_jecDown",
    collectionPostFix = "Puppi_jecDown",
    )


##------------------------------------------
##  Z skim
##------------------------------------------

from CMGTools.TTHAnalysis.analyzers.ttHmllSkimmer import ttHmllSkimmer

genZtautau = cfg.Analyzer(
            ttHmllSkimmer, name='ttHmllSkimmer',
            lepId=[15],
            idCut  = "", # not used
            maxLeps=10, # not used
            massMin=81, # not used
            massMax=101, # not used
            doZGen = True,
            doZReco = False
            )

genZmumu = cfg.Analyzer(
            ttHmllSkimmer, name='ttHmllSkimmer',
            lepId=[13],
            idCut  = "", # not used
            maxLeps=10, # not used
            massMin=81, # not used
            massMax=101, # not used
            doZGen = True,
            doZReco = False
            )

genZee = cfg.Analyzer(
            ttHmllSkimmer, name='ttHmllSkimmer',
            lepId=[11],
            idCut  = "", # not used
            maxLeps=10, # not used
            massMin=81, # not used
            massMax=101, # not used
            doZGen = True,
            doZReco = False
            )

# Tree Producer                                                                                                                                                                         
ttHZskim = cfg.Analyzer(
            ttHmllSkimmer, name='ttHmllSkimmer',
            lepId=[13],
            idCut  = "lepton.relIso03 < 0.2", # can give a cut
            maxLeps=10,
            massMin=81,
            massMax=101,
            doZGen = False,
            doZReco = True
            )


##------------------------------------------
##  Jet selection and  skim
##------------------------------------------

jetAna = cfg.Analyzer(
    JetAnalyzer, name='jetAnalyzer',
    jetCol = 'slimmedJets',
    copyJetsByValue = False,      #Whether or not to copy the input jets or to work with references (should be 'True' if JetAnalyzer is run more than once)
    genJetCol = 'slimmedGenJets',
    rho = ('fixedGridRhoFastjetAll','',''),
    jetPt = 25.,
    jetEta = 4.7,
    jetEtaCentral = 2.4,
    cleanJetsFromLeptons = True,
    jetLepDR = 0.4,
    jetLepArbitration = (lambda jet,lepton : lepton), # you can decide which to keep in case of overlaps; e.g. if the jet is b-tagged you might want to keep the jet
    cleanSelectedLeptons = True, #Whether to clean 'selectedLeptons' after disambiguation. Treat with care (= 'False') if running Jetanalyzer more than once
    minLepPt = 10,
    relaxJetId = True,
    doPuId = False, # Not commissioned in 7.0.X
    recalibrateJets = True, #'MC', # True, False, 'MC', 'Data'
    applyL2L3Residual = True, # Switch to 'Data' when they will become available for Data
    recalibrationType = "AK4PFchs",
    mcGT     = "Spring16_23Sep2016V2_MC",
    dataGT   = [(1,"Spring16_23Sep2016BCDV2_DATA"),(276831,"Spring16_23Sep2016EFV2_DATA"),(278802,"Spring16_23Sep2016GV2_DATA"),(280919,"Spring16_23Sep2016HV2_DATA")],
    jecPath = "${CMSSW_BASE}/src/CMGTools/RootTools/data/jec/",
    shiftJEC = 0, # set to +1 or -1 to apply +/-1 sigma shift to the nominal jet energies
    addJECShifts = False, # if true, add  "corr", "corrJECUp", and "corrJECDown" for each jet (requires uncertainties to be available!)
    smearJets = False,
    shiftJER = 0, # set to +1 or -1 to get +/-1 sigma shifts
    alwaysCleanPhotons = False,
    cleanGenJetsFromPhoton = False,
    cleanJetsFromFirstPhoton = False,
    cleanJetsFromTaus = False,
    cleanJetsFromIsoTracks = False,
    doQG = False,
    do_mc_match = False,
    calculateSeparateCorrections = True, # should be True if recalibrateJets is True, otherwise L1s will be inconsistent
    calculateType1METCorrection  = True,
    type1METParams = { 'jetPtThreshold':15., 'skipEMfractionThreshold':0.9, 'skipMuons':True },
    collectionPostFix = "",
    storeLowPtJets = False,
    )

## Jets Analyzer (generic)
jetAnaScaleUp = jetAna.clone(name='jetAnalyzerScaleUp',
    copyJetsByValue = True,
    jetCol = 'slimmedJets',
    shiftJEC = +1, # set to +1 or -1 to apply +/-1 sigma shift to the nominal jet energies
    collectionPostFix = "_jecUp",
    calculateType1METCorrection  = True,
    cleanSelectedLeptons = False,
   )

## Jets Analyzer (generic)
jetAnaScaleDown = jetAna.clone(name='jetAnalyzerScaleDown',
    copyJetsByValue = True,
    jetCol = 'slimmedJets',
    shiftJEC = -1, # set to +1 or -1 to apply +/-1 sigma shift to the nominal jet energies
    collectionPostFix = "_jecDown",
    calculateType1METCorrection  = True,
    cleanSelectedLeptons = False,
    )


jetPuppiAna = cfg.Analyzer(
    JetAnalyzer, name='jetAnalyzerPuppi',
    jetCol = 'slimmedJetsPuppi',
    copyJetsByValue = False,      #Whether or not to copy the input jets or to work with references (should be 'True' if JetAnalyzer is run more than once)
    genJetCol = 'slimmedGenJets',
    rho = ('fixedGridRhoFastjetAll','',''),
    jetPt = 25.,
    jetEta = 4.7,
    jetEtaCentral = 2.4,
    cleanJetsFromLeptons = True,
    jetLepDR = 0.4,
    jetLepArbitration = (lambda jet,lepton : lepton), # you can decide which to keep in case of overlaps; e.g. if the jet is b-tagged you might want to keep the jet
    cleanSelectedLeptons = True, #Whether to clean 'selectedLeptons' after disambiguation. Treat with care (= 'False') if running Jetanalyzer more than once
    minLepPt = 10,
    relaxJetId = True,
    doPuId = False, # Not commissioned in 7.0.X
    recalibrateJets = True, #'MC', # True, False, 'MC', 'Data'
    applyL2L3Residual = True, # Switch to 'Data' when they will become available for Data
    recalibrationType = "AK4PFPuppi", ## waiting for JEC those not exist yet
    mcGT     = "Spring16_23Sep2016V2_MC",
    dataGT   = [(1,"Spring16_23Sep2016BCDV2_DATA"),(276831,"Spring16_23Sep2016EFV2_DATA"),(278802,"Spring16_23Sep2016GV2_DATA"),(280919,"Spring16_23Sep2016HV2_DATA")],
    jecPath = "${CMSSW_BASE}/src/CMGTools/RootTools/data/jec/",
    shiftJEC = 0, # set to +1 or -1 to apply +/-1 sigma shift to the nominal jet energies
    addJECShifts = False, # if true, add  "corr", "corrJECUp", and "corrJECDown" for each jet (requires uncertainties to be available!)
    smearJets = False,
    shiftJER = 0, # set to +1 or -1 to get +/-1 sigma shifts
    alwaysCleanPhotons = False,
    cleanGenJetsFromPhoton = False,
    cleanJetsFromFirstPhoton = False,
    cleanJetsFromTaus = False,
    cleanJetsFromIsoTracks = False,
    doQG = False,
    do_mc_match = False,
    calculateSeparateCorrections = True, # should be True if recalibrateJets is True, otherwise L1s will be inconsistent
    calculateType1METCorrection  = True,
    type1METParams = { 'jetPtThreshold':15., 'skipEMfractionThreshold':0.9, 'skipMuons':True },
    collectionPostFix = "Puppi",
    storeLowPtJets = False,
    )

## Jets Analyzer (generic)
jetPuppiAnaScaleUp = jetPuppiAna.clone(name='jetAnalyzerPuppiScaleUp',
    copyJetsByValue = True,
    jetCol = 'slimmedJetsPuppi',
    shiftJEC = +1, # set to +1 or -1 to apply +/-1 sigma shift to the nominal jet energies
    collectionPostFix = "Puppi_jecUp",
    calculateType1METCorrection  = True,
    cleanSelectedLeptons = False
   )

## Jets Analyzer (generic)
jetPuppiAnaScaleDown = jetPuppiAna.clone(name='jetAnalyzerPuppiScaleDown',
    copyJetsByValue = True,
    jetCol = 'slimmedJetsPuppi',
    shiftJEC = -1, # set to +1 or -1 to apply +/-1 sigma shift to the nominal jet energies
    collectionPostFix = "Puppi_jecDown",
    calculateType1METCorrection  = True,
    cleanSelectedLeptons = False
    )


# Jet-MET based Skim (generic, but requirements depend on the final state)
from CMGTools.TTHAnalysis.analyzers.ttHJetMETSkimmer import ttHJetMETSkimmer
ttHJetMETSkim = cfg.Analyzer(
   ttHJetMETSkimmer, name='ttHJetMETSkimmer',
   jets      = "cleanJets", # jet collection to use
   jetPtCuts = [50,50],  # e.g. [60,40,30,20] to require at least four jets with pt > 60,40,30,20
   jetVetoPt =  0,  # if non-zero, veto additional jets with pt > veto beyond the ones in jetPtCuts
   metCut    =  0,  # MET cut
   htCut     = ('htJet40j', 0), # cut on HT defined with only jets and pt cut 40, at zero; i.e. no cut
                                # see ttHCoreEventAnalyzer for alternative definitions
   mhtCut    = ('mhtJet40', 0), # cut on MHT defined with all leptons, and jets with pt > 40.
   nBJet     = ('CSVv2IVFM', 0, "jet.pt() > 30"),     # require at least 0 jets passing CSV medium and pt > 30
   )


#-------- SEQUENCE


metCoreSequence = [
    lheWeightAna,
    susyCounter,
    skimAnalyzer,
   #eventSelector,
    jsonAna,
    triggerAna,
    triggerFlagsAna,
    pileUpAna,
    genAna,
    vertexAna,
##### lepton modules below
    lepAna,
   #ttHLepSkim,
   #ttHZskim,
##### photon modules below
    photonAna,
##### jet modules below
    jetAna,
    jetAnaScaleUp,
    jetAnaScaleDown,
    jetPuppiAna,
    jetPuppiAnaScaleUp,
    jetPuppiAnaScaleDown,
##### met modules below
    metAna,
    metAnaScaleUp,
    metAnaScaleDown,
    metPuppiAna,
    metPuppiAnaScaleUp,
    metPuppiAnaScaleDown,
    badChargedHadronAna,
    badMuonAnaMoriond2017,
    badCloneMuonAnaMoriond2017,
    eventFlagsAna,
##    hbheFilterAna,
##### tree
##    treeProducer,
]
