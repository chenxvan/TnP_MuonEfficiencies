import FWCore.ParameterSet.Config as cms
import sys, os, shutil
from optparse import OptionParser
### USAGE: cmsRun fitMuonID.py TEST tight loose mc mc_all
###_id: tight, loose, medium, soft

#_*_*_*_*_*_
#Skimming command:
#../skimTree root://cmseos.fnal.gov//store/user/xuan/MuonTnP/TnPTree_17Nov2017_SingleMuon_Run2017Bv1_Full_GoldenJSON.root TnPTree_17Nov2017_SingleMuon_Run2017Bv1_Full_GoldenJSON.root -r "all" -k "pt eta abseta phi tag_nVertices charge tag_pt tag_eta tag_abseta tag_phi tag_IsoMu27 tag_combRelIsoPF04dBeta tag_bx tag_instLumi l1ptByQ l1drByQ l1qByQ Mu50 HLT_TkMu50 Loose Medium Medium2016 Tight2012 HighPt CutBasedIdGlobalHighPt TM relTkIso combRelIsoPF04dBeta run lumi event mass pair_deltaR pair_probeMultiplicity_Pt10_M60140" -c "tag_IsoMu27==1 && tag_pt > 28.9 && mass > 69.5 && mass < 130.5 && CutBasedIdGlobalHighPt"
#_*_*_*_*_*_

def FillNumDen(num, den):
    '''Declares the needed selections for a givent numerator, denominator'''

    #Define the mass distribution
    if den == "highptid" :
        process.TnP_MuonID.Variables.pair_newTuneP_mass = cms.vstring("Tag-muon Mass", _mrange, "130", "GeV/c^{2}")
    else:
        process.TnP_MuonID.Variables.mass = cms.vstring("Tag-muon Mass", _mrange, "130", "GeV/c^{2}")
    #NUMS
    if num == "looseid":
        process.TnP_MuonID.Categories.PF  = cms.vstring("PF Muon", "dummy[pass=1,fail=0]")
        process.TnP_MuonID.Expressions.Loose_noIPVar  = cms.vstring("Loose_noIPVar", "PF==1", "PF")
        process.TnP_MuonID.Cuts.Loose_noIP = cms.vstring("Loose_noIP", "Loose_noIPVar", "0.5")

    elif num == "mediumid":
        process.TnP_MuonID.Categories.Medium  = cms.vstring("Medium Id.", "dummy[pass=1,fail=0]")
        process.TnP_MuonID.Expressions.Medium_noIPVar= cms.vstring("Medium_noIPVar", "Medium==1", "Medium")
        process.TnP_MuonID.Cuts.Medium_noIP= cms.vstring("Medium_noIP", "Medium_noIPVar", "0.5")

#    elif num == "mediumid":
#        process.TnP_MuonID.Categories.Medium  = cms.vstring("Medium Id. Muon (ICHEP version)", "dummy[pass=1,fail=0]")
#        process.TnP_MuonID.Expressions.Medium_noIPVar= cms.vstring("Medium_noIPVar", "Medium==1", "Medium")
#        process.TnP_MuonID.Cuts.Medium_noIP= cms.vstring("Medium_noIP", "Medium_noIPVar", "0.5")
    elif num == "tightid":
        process.TnP_MuonID.Variables.dzPV  = cms.vstring("dzPV", "-1000", "1000", "")
        process.TnP_MuonID.Categories.Tight2012 = cms.vstring("Tight Id. Muon", "dummy[pass=1,fail=0]")
        process.TnP_MuonID.Expressions.Tight2012_zIPCutVar = cms.vstring("Tight2012_zIPCut", "Tight2012 == 1 && abs(dzPV) < 0.5", "Tight2012", "dzPV")
        process.TnP_MuonID.Cuts.Tight2012_zIPCut = cms.vstring("Tight2012_zIPCut", "Tight2012_zIPCutVar", "0.5")

########
#    elif num == "tklooseiso":
#        process.TnP_MuonID.Variables.relTkIso = cms.vstring("trk rel iso dR 0.3", "-2", "9999999", "")
#        process.TnP_MuonID.Cuts.LooseTkIso3 = cms.vstring("LooseTkIso3" ,"relTkIso", "0.10")


    elif num == "triggerid":
        process.TnP_MuonID.Variables.dzPV  = cms.vstring("dzPV", "-1000", "1000", "")
        process.TnP_MuonID.Categories.HighPt = cms.vstring("High-pT Id. Muon", "dummy[pass=1,fail=0]")
        process.TnP_MuonID.Variables.relTkIso = cms.vstring("trk rel iso dR 0.3", "-2", "9999999", "")
        process.TnP_MuonID.Categories.Mu50 = cms.vstring("HLT Mu50", "dummy[pass=1,fail=0]")
        process.TnP_MuonID.Categories.OldMu100 = cms.vstring("OldMu100", "dummy[pass=1,fail=0]")
        process.TnP_MuonID.Categories.TkMu100 = cms.vstring("TkMu100", "dummy[pass=1,fail=0]")
        process.TnP_MuonID.Categories.HLT_TkMu50 = cms.vstring("HLT tkMu50", "dummy[pass=1,fail=0]")
        #for 2017
#        process.TnP_MuonID.Expressions.Trigger_CutVar = cms.vstring("Trigger_Cut", "Mu50 == 1", "Mu50", "HLT_TkMu50", "dzPV")
        #for 2018
        process.TnP_MuonID.Expressions.Trigger_CutVar = cms.vstring("Trigger_Cut", "Mu 50 == 1 || TkMu100 == 1 || OldMu100", "Mu50", "OldMu100", "TkMu100")
        process.TnP_MuonID.Cuts.Trigger_Cut = cms.vstring("Trigger_Cut", "Trigger_CutVar", "0.5")

    elif num == "tightidhww":
        process.TnP_MuonID.Variables.dzPV  = cms.vstring("dzPV", "-1000", "1000", "")
        process.TnP_MuonID.Variables.dB  = cms.vstring("dB", "-1000", "1000", "")
        process.TnP_MuonID.Categories.Tight2012 = cms.vstring("Tight Id. HWW Muon", "dummy[pass=1,fail=0]")
        process.TnP_MuonID.Expressions.Tight2012_zIPdBCutVar = cms.vstring("Tight2012_zIPdBCut", "Tight2012 == 1 && abs(dzPV) < 0.1 && abs(dB) < 0.02", "Tight2012", "dzPV", "dB")
        process.TnP_MuonID.Cuts.Tight2012_zIPdBCut = cms.vstring("Tight2012_zIPdBCut", "Tight2012_zIPdBCutVar", "0.5")
    elif num == "highptid":
        process.TnP_MuonID.Variables.dzPV  = cms.vstring("dzPV", "-1000", "1000", "")
        process.TnP_MuonID.Categories.HighPt = cms.vstring("High-pT Id. Muon", "dummy[pass=1,fail=0]")
        process.TnP_MuonID.Expressions.HighPt_zIPCutVar = cms.vstring("HighPt_zIPCut", "HighPt == 1 && abs(dzPV) < 0.5", "HighPt", "dzPV")
        process.TnP_MuonID.Cuts.HighPt_zIPCut = cms.vstring("HighPt_zIPCut", "HighPt_zIPCutVar", "0.5")
    elif num == "looseiso":
        process.TnP_MuonID.Variables.combRelIsoPF04dBeta = cms.vstring("dBeta rel iso dR 0.4", "-2", "9999999", "")
        process.TnP_MuonID.Cuts.LooseIso4 = cms.vstring("LooseIso4" ,"combRelIsoPF04dBeta", "0.25")
    elif num == "tightiso":
        process.TnP_MuonID.Variables.combRelIsoPF04dBeta = cms.vstring("dBeta rel iso dR 0.4", "-2", "9999999", "")
        process.TnP_MuonID.Cuts.TightIso4 = cms.vstring("TightIso4" ,"combRelIsoPF04dBeta", "0.15")
    elif num == "tklooseiso":
        process.TnP_MuonID.Variables.relTkIso = cms.vstring("trk rel iso dR 0.3", "-2", "9999999", "")
        process.TnP_MuonID.Cuts.LooseTkIso3 = cms.vstring("LooseTkIso3" ,"relTkIso", "0.10")
    #DEN
    if den == "looseid":
        process.TnP_MuonID.Categories.PF  = cms.vstring("PF Muon", "dummy[pass=1,fail=0]")
    elif den == "mediumid":
        process.TnP_MuonID.Categories.Medium = cms.vstring("Medium Id.", "dummy[pass=1,fail=0]")
    elif den == "tightid":
        process.TnP_MuonID.Variables.dzPV  = cms.vstring("dzPV", "-1000", "1000", "")
        process.TnP_MuonID.Categories.Tight2012 = cms.vstring("Tight Id. Muon", "dummy[pass=1,fail=0]")
    elif den == "tightidhww":
        process.TnP_MuonID.Variables.dzPV  = cms.vstring("dzPV", "-1000", "1000", "")
        process.TnP_MuonID.Variables.dB  = cms.vstring("dB", "-1000", "1000", "")
        process.TnP_MuonID.Categories.Tight2012 = cms.vstring("Tight Id. HWW Muon", "dummy[pass=1,fail=0]")
        process.TnP_MuonID.Expressions.Tight2012_zIPdBCutVar = cms.vstring("Tight2012_zIPdBCut", "Tight2012 == 1 && abs(dzPV) < 0.1 && abs(dB) < 0.02", "Tight2012", "dzPV", "dB")
        process.TnP_MuonID.Cuts.Tight2012_zIPdBCut = cms.vstring("Tight2012_zIPdBCut", "Tight2012_zIPdBCutVar", "0.5")
    elif den == "highptid":
        process.TnP_MuonID.Variables.dzPV  = cms.vstring("dzPV", "-1000", "1000", "")
        process.TnP_MuonID.Categories.HighPt = cms.vstring("High-pT Id. Muon", "dummy[pass=1,fail=0]")
        process.TnP_MuonID.Expressions.HighPt_zIPCutVar = cms.vstring("HighPt_zIPCut", "HighPt == 1 && abs(dzPV) < 0.5", "HighPt", "dzPV")
        process.TnP_MuonID.Cuts.HighPt_zIPCut = cms.vstring("HighPt_zIPCut", "HighPt_zIPCutVar", "0.5")



def FillVariables(par):
    '''Declares only the parameters which are necessary, no more'''

    if par == 'newpt' or 'newpt_eta':
        process.TnP_MuonID.Variables.pair_newTuneP_probe_pt = cms.vstring("muon p_{T} (tune-P)", "0", "1000", "GeV/c")
    if par == 'eta':
        process.TnP_MuonID.Variables.eta  = cms.vstring("muon #eta", "-2.5", "2.5", "")
    if par == 'pt' or 'pt_eta' or 'pt_eta_id' or 'pt_eta_hlt' or 'pt_eta_hlt_fine':
        process.TnP_MuonID.Variables.pt  = cms.vstring("muon p_{T}", "0", "1000", "GeV/c")
    if par == 'pt_eta' or 'newpt_eta' or 'pt_eta_id' or 'pt_eta_hlt' or 'pt_eta_hlt_fine':
        process.TnP_MuonID.Variables.abseta  = cms.vstring("muon |#eta|", "0", "2.5", "")
    if par == 'tag_instLumi':
        process.TnP_MuonID.Variables.tag_instLumi  = cms.vstring("Inst. Lumi [10E30]", "0", "15", "")
    if par == 'pair_deltaR':
        process.TnP_MuonID.Variables.pair_deltaR  = cms.vstring("deltaR", "0", "4", "")
    if par == 'vtx':
        print 'I filled it'
        process.TnP_MuonID.Variables.tag_nVertices   = cms.vstring("Number of vertices", "0", "999", "")

def FillBin(par):
    '''Sets the values of the bin paramters and the bool selections on the denominators'''
    #Parameter
    if par == 'eta':
        DEN.eta = cms.vdouble(-2.4, -2.1, -1.6, -1.2, -0.9, -0.3, -0.2, 0.2, 0.3, 0.9, 1.2, 1.6, 2.1, 2.4)
    elif par == 'pt':
#        DEN.pt = cms.vdouble(20, 25, 30, 40, 50, 60, 120)
#        DEN.pt = cms.vdouble(20, 25, 30, 40, 50, 55, 60, 120,200) DEFAULT
        DEN.pt = cms.vdouble(2.0, 2.5, 2.75, 3.0, 3.25, 3.5, 3.75, 4.0, 4.5, 5.0, 6.0, 8.0, 10.0, 15.0, 20.0, 25.0, 30.0, 40.0, 50.0, 60.0, 120.0, 200.0, 300.0, 500.0, 700.0, 1200.0)
    elif par == 'pt_eta':
#        DEN.pt = cms.vdouble(20, 25, 30, 40, 50, 60, 120) PRESENTATION 170710: same for newpt_eta
        DEN.pt = cms.vdouble(2.0, 2.5,  2.75, 3, 3.25, 3.5, 3.75, 4.0, 4.5, 5.0, 6.0, 8.0, 10.0, 15.0, 20.0, 25.0, 30.0, 40.0, 50.0, 60.0, 120.0, 200.0, 300.0, 500.0, 700.0, 1200.0)
        DEN.abseta = cms.vdouble( 0., 0.9, 1.2, 2.1, 2.4)
    elif par == 'pt_eta_id':
        DEN.pt = cms.vdouble(20.0, 25.0, 30.0, 40.0, 50.0, 60.0, 120.0)
        DEN.abseta = cms.vdouble(0.0, 0.9, 1.2, 2.1, 2.4)
    elif par == 'pt_eta_hlt':
#        DEN.pt = cms.vdouble(50.0, 80.0, 120.0, 200.0, 300.0, 400.0, 800.0)
#        DEN.pt = cms.vdouble(52.0, 55.0, 60.0, 80.0, 120.0, 800.0)
        DEN.pt = cms.vdouble(52.0, 56.0, 60.0, 120.0, 200.0, 300.0, 1200.0) 
        DEN.abseta = cms.vdouble(0.0, 0.9, 1.2, 2.1, 2.4)
    elif par == 'pt_eta_hlt_fine':
        DEN.pt = cms.vdouble(52.0, 55.0, 60.0, 80.0, 120.0, 200.0, 300.0, 400.0, 800.0)
        DEN.abseta = cms.vdouble(0.0, 0.9, 1.2, 2.1, 2.4)


args = sys.argv[1:]
iteration = ''
if len(args) > 1: iteration = args[1]
print "The iteration is", iteration
num = 'tight'
if len(args) > 2: num = args[2]
print 'The num is', num
den = 'tight'
if len(args) > 3: den = args[3]
print 'The den is', den
scenario = "data_all"
if len(args) > 4: scenario = args[4]
print "Will run scenario ", scenario
sample = 'data'
if len(args) > 5: sample = args[5]
print 'The sample is', sample
if len(args) > 6: par = args[6]
print 'The binning is', par
bgFitFunction = 'default'
if len(args) > 7: bgFitFunction = args[7]
if bgFitFunction == 'CMSshape':
    print 'Will use the CMS shape to fit the background'
elif bgFitFunction == 'custom':
    print 'Will experiment with custom fit functions'
elif bgFitFunction == 'default':
    print 'Will use the standard fit functions for the backgroud'
else:
    print 'Will use',bgFitFunction,"to fit background"


process = cms.Process("TagProbe")
process.load('FWCore.MessageService.MessageLogger_cfi')
process.source = cms.Source("EmptySource")
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )

if not num  in ['looseid', 'mediumid', 'tightid', 'triggerid', 'tightidhww', 'puppiIso', 'puppiIsoNoLep', 'combpuppiIso','muCleanerIII', 'muCleanerIV', 'highptid', 'looseiso', 'tightiso', 'tklooseiso']:
    print '@ERROR: num should be in ',['looseid', 'mediumid', 'tightid', 'triggerid', 'tightidhww', 'puppiIso', 'puppiIsoNoLep', 'combpuppiIso', 'muCleanerIII', 'muCleanerIV', 'highptid', 'looseiso', 'tightiso', 'tklooseiso'], 'You used', num, '.Abort'
    sys.exit()
if not den in ['looseid', 'mediumid', 'tightid', 'tightidhww', 'highptid', 'gentrack']:
    print '@ERROR: den should be',['looseid', 'mediumid', 'tightid', 'tightidhww', 'highptid'], 'You used', den, '.Abort'
    sys.exit()
if not par in  ['pt', 'eta', 'vtx', 'pt_eta', 'newpt', 'newpt_eta', 'tag_instLumi', 'pair_deltaR', 'pt_eta_id', 'pt_eta_hlt', 'pt_eta_hlt_fine']:
    print '@ERROR: par should be', ['pt', 'eta', 'vtx', 'pt_eta', 'newpt', 'newpt_eta', 'tag_instLumi', 'pair_deltaR', 'pt_eta_id', 'pt_eta_hlt', 'pt_eta_hlt_fine'], 'You used', par, '.Abort'

#_*_*_*_*_*_*_*_*_*_*_*_*
#Prepare variables, den, num and fit funct
#_*_*_*_*_*_*_*_*_*_*_*_*

#Set-up the mass range
_mrange = "70"
if 'iso' in num:
    _mrange = "77"
print '_mrange is', _mrange
mass_ =" mass"
if den == "highptid" : mass_ = "pair_newTuneP_mass"



Template = cms.EDAnalyzer("TagProbeFitTreeAnalyzer",
                          NumCPU = cms.uint32(1),
    SaveWorkspace = cms.bool(False),


    Variables = cms.PSet(
        #essential for all den/num
        #mass = cms.vstring("Tag-muon Mass", _mrange, "130", "GeV/c^{2}"),
        #Jeta    = cms.vstring("muon #eta", "-2.5", "2.5", ""),
        ),

    Categories = cms.PSet(),
    Expressions = cms.PSet(),
    Cuts = cms.PSet(),


    PDFs = cms.PSet(
        voigtPlusExpo = cms.vstring(
            "Voigtian::signal(mass, mean[90,80,100], width[2.495], sigma[3,1,20])".replace("mass",mass_),
            "Exponential::backgroundPass(mass, lp[0,-5,5])".replace("mass",mass_),
            "Exponential::backgroundFail(mass, lf[0,-5,5])".replace("mass",mass_),
            "efficiency[0.9,0,1]",
            "signalFractionInPassing[0.9]"
        ),
        vpvPlusExpo = cms.vstring(
            "Voigtian::signal1(mass, mean1[90,80,100], width[2.495], sigma1[2,1,3])".replace("mass",mass_),
            "Voigtian::signal2(mass, mean2[90,80,100], width,        sigma2[4,2,10])".replace("mass",mass_),
            "SUM::signal(vFrac[0.8,0,1]*signal1, signal2)",
            "Exponential::backgroundPass(mass, lp[-0.1,-1,0.1])".replace("mass",mass_),
            "Exponential::backgroundFail(mass, lf[-0.1,-1,0.1])".replace("mass",mass_),
            "efficiency[0.9,0,1]",
            "signalFractionInPassing[0.9]"
        ),
        vpvPlusExpo3 = cms.vstring(
            "Voigtian::signalPass1(mass, meanPass1[91,84,98], width[2.495], sigmaPass1[2.5,1,6])".replace("mass",mass_),
            "Voigtian::signalPass2(mass, meanPass2[91,81,101], width,        sigmaPass2[5,1,10])".replace("mass",mass_),
            "SUM::signalPass(vFracPass[0.8,0,1]*signalPass1, signalPass2)",
            "Voigtian::signalFail1(mass, meanFail1[91,84,98], width[2.495], sigmaFail1[2.5,1,6])".replace("mass",mass_),
            "Voigtian::signalFail2(mass, meanFail2[91,81,101], width,        sigmaFail2[5,1,10])".replace("mass",mass_),
            "SUM::signalFail(vFracFail[0.8,0,1]*signalFail1, signalFail2)",
            "Exponential::backgroundPass(mass, lp[-0.1,-1,0.1])".replace("mass",mass_),
            "Exponential::backgroundFail(mass, lf[-0.1,-1,0.1])".replace("mass",mass_),
            "efficiency[0.9,0,1]",
            "signalFractionInPassing[0.9]"
        ),




        vpvPlusExpoMin70 = cms.vstring(
            "Voigtian::signal1(mass, mean1[90,80,100], width[2.495], sigma1[2,1,3])".replace("mass",mass_),
            "Voigtian::signal2(mass, mean2[90,80,100], width,        sigma2[4,3,10])".replace("mass",mass_),
            "SUM::signal(vFrac[0.8,0.5,1]*signal1, signal2)",
            "Exponential::backgroundPass(mass, lp[-0.1,-1,0.1])".replace("mass",mass_),
            "Exponential::backgroundFail(mass, lf[-0.1,-1,0.1])".replace("mass",mass_),
            "efficiency[0.9,0.7,1]",
            "signalFractionInPassing[0.9]"
        ),
        vpvPlusCheb = cms.vstring(
            "Voigtian::signal1(mass, mean1[90,80,100], width[2.495], sigma1[2,1,3])".replace("mass",mass_),
            "Voigtian::signal2(mass, mean2[90,80,100], width,        sigma2[4,3,10])".replace("mass",mass_),
            "SUM::signal(vFrac[0.8,0.5,1]*signal1, signal2)",
            #par3
            "RooChebychev::backgroundPass(mass, {a0[0.25,0,0.5], a1[-0.25,-1,0.1],a2[0.,-0.25,0.25]})".replace("mass",mass_),
            "RooChebychev::backgroundFail(mass, {a0[0.25,0,0.5], a1[-0.25,-1,0.1],a2[0.,-0.25,0.25]})".replace("mass",mass_),
            "efficiency[0.9,0.7,1]",
            "signalFractionInPassing[0.9]"
        ),
        vpvPlusCMS = cms.vstring(
            "Voigtian::signal1(mass, mean1[90,80,100], width[2.495], sigma1[2,1,3])".replace("mass",mass_),
            "Voigtian::signal2(mass, mean2[90,80,100], width,        sigma2[4,3,10])".replace("mass",mass_),
            "SUM::signal(vFrac[0.8,0.5,1]*signal1, signal2)",
            "RooCMSShape::backgroundPass(mass, alphaPass[70.,60.,90.], betaPass[0.02, 0.01,0.1], gammaPass[0.001, 0.,0.1], peakPass[90.0])".replace("mass",mass_),
            "RooCMSShape::backgroundFail(mass, alphaFail[70.,60.,90.], betaFail[0.02, 0.01,0.1], gammaFail[0.001, 0.,0.1], peakPass)".replace("mass",mass_),
            "efficiency[0.9,0.7,1]",
            "signalFractionInPassing[0.9]"
        ),
        vpvPlusCMSbeta0p2 = cms.vstring(
            "Voigtian::signal1(mass, mean1[90,80,100], width[2.495], sigma1[2,1,3])".replace("mass",mass_),
            "Voigtian::signal2(mass, mean2[90,80,100], width,        sigma2[4,3,10])".replace("mass",mass_),
            "RooCMSShape::backgroundPass(mass, alphaPass[70.,60.,90.], betaPass[0.001, 0.,0.1], gammaPass[0.001, 0.,0.1], peakPass[90.0])".replace("mass",mass_),
            "RooCMSShape::backgroundFail(mass, alphaFail[70.,60.,90.], betaFail[0.03, 0.02,0.1], gammaFail[0.001, 0.,0.1], peakPass)".replace("mass",mass_),
            #"RooCMSShape::backgroundPass(mass, alphaPass[70.,60.,90.], betaPass[0.001, 0.01,0.1], gammaPass[0.001, 0.,0.1], peakPass[90.0])".replace("mass",mass_),
            #"RooCMSShape::backgroundFail(mass, alphaFail[70.,60.,90.], betaFail[0.001, 0.01,0.1], gammaFail[0.001, 0.,0.1], peakPass)".replace("mass",mass_),
            "SUM::signal(vFrac[0.8,0.5,1]*signal1, signal2)",
            "efficiency[0.9,0.7,1]",
            "signalFractionInPassing[0.9]"
        )
    ),

    binnedFit = cms.bool(True),
    binsForFit = cms.uint32(40),
    saveDistributionsPlot = cms.bool(False),

    Efficiencies = cms.PSet(), # will be filled later
)
if sample == "data_runa":
    process.TnP_MuonID = Template.clone(
        InputFileNames = cms.vstring(
            '/uscms_data/d3/xuan/MuonTnP/CMSSW_10_2_5/src/TnPUtils/our_withPT/TnPTreeZ_17Sep2018_SingleMuon_Run2018Av2_GoldenJSON.root'
            ),
        InputTreeName = cms.string("fitter_tree"),
        InputDirectoryName = cms.string("tpTree"),
        OutputFileName = cms.string("TnP_Muon_RunB_%s.root" % scenario),
        Efficiencies = cms.PSet(),
        ) 


if sample == "data_runb":
    process.TnP_MuonID = Template.clone(
        InputFileNames = cms.vstring(
            '/uscms_data/d3/xuan/MuonTnP/CMSSW_10_2_5/src/TnPUtils/our_withPT/TnPTreeZ_17Sep2018_SingleMuon_Run2018Bv1_GoldenJSON.root'
            ),
        InputTreeName = cms.string("fitter_tree"),
        InputDirectoryName = cms.string("tpTree"),
        OutputFileName = cms.string("TnP_Muon_RunB_%s.root" % scenario),
        Efficiencies = cms.PSet(),
        )

if sample == "data_runc":
    process.TnP_MuonID = Template.clone(
        InputFileNames = cms.vstring(
            '/uscms_data/d3/xuan/MuonTnP/CMSSW_10_2_5/src/TnPUtils/test_wo_tag_iso/TnPTreeZ_17Sep2018_SingleMuon_Run2018Cv1_GoldenJSON.root'
            ),
        InputTreeName = cms.string("fitter_tree"),
        InputDirectoryName = cms.string("tpTree"),
        OutputFileName = cms.string("TnP_Muon_RunC_%s.root" % scenario),
        Efficiencies = cms.PSet(),
        )

if sample == "data_rund":
    process.TnP_MuonID = Template.clone(
        InputFileNames = cms.vstring(
            '/uscms_data/d3/xuan/MuonTnP/CMSSW_10_2_5/src/TnPUtils/our_withPT/TnPTreeZ_SingleMuon_Run2018Dv2_GoldenJSON.root'
            ),
        InputTreeName = cms.string("fitter_tree"),
        InputDirectoryName = cms.string("tpTree"),
        OutputFileName = cms.string("TnP_Muon_RunD_%s.root" % scenario),
        Efficiencies = cms.PSet(),
        )

if sample == "data_rune":
    process.TnP_MuonID = Template.clone(
        InputFileNames = cms.vstring(
            '/uscms_data/d3/xuan/MuonTnP/CMSSW_9_4_0_pre3/src/TnPUtils/official_test/TnPTree_17Nov2017_SingleMuon_Run2017Ev1_Full_GoldenJSON.root'
            ),
        InputTreeName = cms.string("fitter_tree"),
        InputDirectoryName = cms.string("tpTree"),
        OutputFileName = cms.string("TnP_Muon_RunE_%s.root" % scenario),
        Efficiencies = cms.PSet(),
        )

if sample == "data_runf":
    process.TnP_MuonID = Template.clone(
        InputFileNames = cms.vstring(
            '/uscms_data/d3/xuan/MuonTnP/CMSSW_9_4_0_pre3/src/TnPUtils/official_test/TnPTree_17Nov2017_SingleMuon_Run2017Fv1_Full_GoldenJSON.root'
            ),
        InputTreeName = cms.string("fitter_tree"),
        InputDirectoryName = cms.string("tpTree"),
        OutputFileName = cms.string("TnP_Muon_RunF_%s.root" % scenario),
        Efficiencies = cms.PSet(),
        )


if sample == "data_runbf":
    process.TnP_MuonID = Template.clone(
        InputFileNames = cms.vstring(
            '/uscms_data/d3/xuan/MuonTnP/CMSSW_9_4_0_pre3/src/TnPUtils/official_test/TnPTree_17Nov2017_SingleMuon_Run2017Bv1_Full_GoldenJSON.root',
            '/uscms_data/d3/xuan/MuonTnP/CMSSW_9_4_0_pre3/src/TnPUtils/official_test/TnPTree_17Nov2017_SingleMuon_Run2017Cv1_Full_GoldenJSON.root',
            '/uscms_data/d3/xuan/MuonTnP/CMSSW_9_4_0_pre3/src/TnPUtils/official_test/TnPTree_17Nov2017_SingleMuon_Run2017Dv1_Full_GoldenJSON.root',
            '/uscms_data/d3/xuan/MuonTnP/CMSSW_9_4_0_pre3/src/TnPUtils/official_test/TnPTree_17Nov2017_SingleMuon_Run2017Ev1_Full_GoldenJSON.root',
            '/uscms_data/d3/xuan/MuonTnP/CMSSW_9_4_0_pre3/src/TnPUtils/official_test/TnPTree_17Nov2017_SingleMuon_Run2017Fv1_Full_GoldenJSON.root'
            ),
        InputTreeName = cms.string("fitter_tree"),
        InputDirectoryName = cms.string("tpTree"),
        OutputFileName = cms.string("TnP_Muon_RunBF_%s.root" % scenario),
        Efficiencies = cms.PSet(),
        )


if sample == "dataall":
    process.TnP_MuonID = Template.clone(
        InputFileNames = cms.vstring(
            'root://cmseos.fnal.gov//store/user/drberry/MuonTagAndProbe/Skims/TnPTree_80XRereco_Run2016_All_GoldenJSON_Run276098to276384.root'
            ),
        InputTreeName = cms.string("fitter_tree"),
        InputDirectoryName = cms.string("tpTree"),
        OutputFileName = cms.string("TnP_Muon_%s.root" % scenario),
        Efficiencies = cms.PSet(),
        )

if sample == "mcall":
    process.TnP_MuonID = Template.clone(
        InputFileNames = cms.vstring(
            '/uscms_data/d3/xuan/MuonTnP/CMSSW_10_2_5/src/TnPUtils/our_withPT/TnPTreeZ_102XAutumn18_DYJetsToLL_M50_MadgraphMLM.root'
            ),
        InputTreeName = cms.string("fitter_tree"),
        InputDirectoryName = cms.string("tpTree"),
        OutputFileName = cms.string("TnP_Muon_%s.root" % scenario),
        Efficiencies = cms.PSet(),
        )

if scenario == "mc_all":
    print "Including the weight for MC"
    process.TnP_MuonID.WeightVariable = cms.string("weight")
    process.TnP_MuonID.Variables.weight = cms.vstring("weight","0","10","")


BIN = cms.PSet(
        )

print 'debug1'
Num_dic = {'looseid':'LooseID','mediumid':'MediumID','tightid':'TightID','triggerid':'TriggerID','tightidhww':'TightIDHWW','puppiIso':'PuppiIso','puppiIsoNoLep':'PuppiIsoNoLep','combpuppiIso':'combPuppiIso', 'muCleanerIII':'MuonCleanerIII', 'muCleanerIV':'MuonCleanerIV', 'highptid':'HighPtID','looseiso':'LooseRelIso','tightiso':'TightRelIso','tklooseiso':'LooseRelTkIso'}
Den_dic = {'gentrack':'genTracks','looseid':'LooseID','mediumid':'MediumID','tightid':'TightIDandIPCut','tightidhww':'TightIDHWW','highptid':'HighPtIDandIPCut'}
Sel_dic = {'looseid':'Loose_noIP','mediumid':'Medium_noIP','tightid':'Tight2012_zIPCut','triggerid':'Trigger_Cut','tightidhww':'Tight2012_zIPdBCut','puppiIso':'puppiIsoCut', 'puppiIsoNoLep':'puppiIsoNoLepCut','combpuppiIso':'combpuppiIsoCut','muCleanerIII':'TM_cleanMuonIIICut', 'muCleanerIV':'TM_cleanMuonIVCut', 'highptid':'HighPt_zIPCut','looseiso':'LooseIso4','tightiso':'TightIso4','tklooseiso':'LooseTkIso3'}

#Par_dic = {'eta':'eta', 'pt':}

FillVariables(par)
FillNumDen(num,den)

#process.TnP_MuonID.Categories = cms.PSet(
#    PF  = cms.vstring("PF Muon", "dummy[pass=1,fail=0]")
#    )
#process.TnP_MuonID.Expressions = cms.PSet(
#    Loose_noIPVar  = cms.vstring("Loose_noIPVar", "PF==1", "PF")
#    )
#process.TnP_MuonID.Cuts = cms.PSet(
#    Loose_noIP = cms.vstring("Loose_noIP", "Loose_noIPVar", "0.5")
#    )

#process.TnP_MuonID.Categories.PF  = cms.vstring("PF Muon", "dummy[pass=1,fail=0]")
#process.TnP_MuonID.Expressions.Loose_noIPVar  = cms.vstring("Loose_noIPVar", "PF==1", "PF")
#process.TnP_MuonID.Cuts.Loose_noIP = cms.vstring("Loose_noIP", "Loose_noIPVar", "0.5")



#Template.Categories.PF  = cms.vstring("PF Muon", "dummy[pass=1,fail=0]"),
#Template.Expression.Loose_noIPVar  = cms.vstring("Loose_noIPVar", "PF==1", "PF")
#Template.Cuts.Loose_noIP = cms.vstring("Loose_noIP", "Loose_noIPVar", "0.5")

print 'den is', den,'dic',Den_dic[den]
print 'num is', num,'dic',Num_dic[num]
print 'par is', par

ID_BINS = [(Sel_dic[num],("NUM_%s_DEN_%s_PAR_%s"%(Num_dic[num],Den_dic[den],par),BIN))]
print 'debug5'

print Sel_dic[num]
print ("NUM_%s_DEN_%s_PAR_%s"%(Num_dic[num],Den_dic[den],par),BIN)

#_*_*_*_*_*_*_*_*_*_*_*
#Launch fit production
#_*_*_*_*_*_*_*_*_*_*_*

for ID, ALLBINS in ID_BINS:
    print 'debug1'
    X = ALLBINS[0]
    B = ALLBINS[1]
    _output = os.getcwd() + '/Efficiency' + iteration
    if not os.path.exists(_output):
        print 'Creating', '/Efficiency' + iteration,', the directory where the fits are stored.'
        os.makedirs(_output)
    if scenario == 'data_all':
        _output += '/DATA' + '_' + sample
    elif scenario == 'mc_all':
        _output += '/MC' + '_' + sample
    if not os.path.exists(_output):
        os.makedirs(_output)
    module = process.TnP_MuonID.clone(OutputFileName = cms.string(_output + "/TnP_%s_%s_%s.root" % (scenario,X,bgFitFunction)))
    #save the fitconfig in the plot directory
#    shutil.copyfile(os.getcwd()+'/fitMuon2_Doug.py',_output+'/fitMuon2_Doug.py')
    shape = cms.vstring(bgFitFunction)
    print 'debug2',shape



    DEN = B.clone(); num_ = ID;
    FillBin(par)

    if not "iso" in num: #customize only for ID
        if bgFitFunction == 'default':
            if ('pt' in X):
                print 'den is', den
                print 'num is ', num
                print 'X is ', X
                if ('TriggerID' in X):
                    if scenario == "mc_all": shape = cms.vstring("vpvPlusCMSbeta0p2","*pt_bin4*","vpvPlusExpo")
                    else: shape = cms.vstring("vpvPlusExpo3")
#                    else: shape = cms.vstring("vpvPlusCMS","*pt_bin3*","vpvPlusCheb","*pt_bin4*","vpvPlusExpo")
                elif ('TightID' in X):
                    if scenario == "mc_all": shape = cms.vstring("vpvPlusCMSbeta0p2")
                    else: shape = cms.vstring("vpvPlusCMS")
                else:
                    print 'Running default id'
                    if scenario == "mc_all": shape = cms.vstring("vpvPlusCMSbeta0p2")
                    else: shape = cms.vstring("vpvPlusCMS")
        elif bgFitFunction == 'CMSshape':
            if den == "highpt":
                if (len(DEN.pair_newTuneP_probe_pt)==9):
                    shape = cms.vstring("vpvPlusExpo","*pt_bin4*","vpvPlusCMS","*pt_bin5*","vpvPlusCMS","*pt_bin6*","vpvPlusCheb","*pt_bin7*","vpvPlusCheb")
            else:
                if (len(DEN.pt)==8):
                    shape = cms.vstring("vpvPlusExpo","*pt_bin4*","vpvPlusCMS","*pt_bin5*","vpvPlusCheb","*pt_bin6*","vpvPlusCheb")


    print 'd3'
    mass_variable ="mass"
    print 'den is', den
    if den == "highptid" :
        mass_variable = "pair_newTuneP_mass"
    #compute isolation efficiency
    if scenario == 'data_all':
        if num_.find("Iso4") != -1 or num_.find("Iso3") != -1:
            setattr(module.Efficiencies, ID+"_"+X, cms.PSet(
                EfficiencyCategoryAndState = cms.vstring(num_,"below"),
                UnbinnedVariables = cms.vstring(mass_variable),
                BinnedVariables = DEN,
                BinToPDFmap = shape
                ))
        else:
            print 'd4'
            setattr(module.Efficiencies, ID+"_"+X, cms.PSet(
                EfficiencyCategoryAndState = cms.vstring(num_,"above"),
                UnbinnedVariables = cms.vstring(mass_variable),
                BinnedVariables = DEN,
                BinToPDFmap = shape
                ))
        setattr(process, "TnP_MuonID_"+ID+"_"+X, module)
        setattr(process, "run_"+ID+"_"+X, cms.Path(module))
        if num_.find("puppiIso") != -1:
            setattr(module.Efficiencies, ID+"_"+X, cms.PSet(
                    EfficiencyCategoryAndState = cms.vstring(num_,"below"),
                    UnbinnedVariables = cms.vstring(mass_variable),
                    BinnedVariables = DEN,
                    BinToPDFmap = shape
                    ))
    elif scenario == 'mc_all':
        if num_.find("Iso4") != -1 or num_.find("Iso3") != -1:
            setattr(module.Efficiencies, ID+"_"+X, cms.PSet(
                EfficiencyCategoryAndState = cms.vstring(num_,"below"),
                UnbinnedVariables = cms.vstring(mass_variable,"weight"),
                BinnedVariables = DEN,
                BinToPDFmap = shape
                ))
        else:
            setattr(module.Efficiencies, ID+"_"+X, cms.PSet(
                EfficiencyCategoryAndState = cms.vstring(num_,"above"),
                UnbinnedVariables = cms.vstring(mass_variable,"weight"),
                BinnedVariables = DEN,
                BinToPDFmap = shape
                ))
        setattr(process, "TnP_MuonID_"+ID+"_"+X, module)
        setattr(process, "run_"+ID+"_"+X, cms.Path(module))
        if num_.find("puppiIso") != -1:
             setattr(module.Efficiencies, ID+"_"+X, cms.PSet(
                    EfficiencyCategoryAndState = cms.vstring(num_,"below"),
                    UnbinnedVariables = cms.vstring(mass_variable,"weight"),
                        BinnedVariables = DEN,
                    BinToPDFmap = shape
                    ))
