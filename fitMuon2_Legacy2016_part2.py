import FWCore.ParameterSet.Config as cms
import sys, os, shutil
from optparse import OptionParser
### USAGE: cmsRun fitMuonID.py TEST tight loose mc mc_all
###_id: tight, loose, medium, soft

#_*_*_*_*_*_
#Read Inputs
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
    elif num == "tightidhww":
        process.TnP_MuonID.Variables.dzPV  = cms.vstring("dzPV", "-1000", "1000", "")
        process.TnP_MuonID.Variables.dB  = cms.vstring("dB", "-1000", "1000", "")
        process.TnP_MuonID.Categories.Tight2012 = cms.vstring("Tight Id. HWW Muon", "dummy[pass=1,fail=0]")
        process.TnP_MuonID.Expressions.Tight2012_zIPdBCutVar = cms.vstring("Tight2012_zIPdBCut", "Tight2012 == 1 && abs(dzPV) < 0.1 && abs(dB) < 0.02", "Tight2012", "dzPV", "dB")
        process.TnP_MuonID.Cuts.Tight2012_zIPdBCut = cms.vstring("Tight2012_zIPdBCut", "Tight2012_zIPdBCutVar", "0.5")
    elif num == "puppiIso":
        process.TnP_MuonID.Variables.pt = cms.vstring("pt", "0.0", "999", "")
        process.TnP_MuonID.Variables.muPFIsoValueCHR04PUPPI = cms.vstring("muPFIsoValueCHR04PUPPI", "-1.0", "99999999","")
        process.TnP_MuonID.Variables.muPFIsoValueNHR04PUPPI = cms.vstring("muPFIsoValueNHR04PUPPI","-1.0",  "99999999", "")
        process.TnP_MuonID.Variables.muPFIsoValuePhR04PUPPI = cms.vstring("muPFIsoValuePhR04PUPPI", "-1.0", "99999999", "")
        process.TnP_MuonID.Expressions.puppiIsoVar = cms.vstring("puppiIsoVar", "(muPFIsoValueCHR04PUPPI+muPFIsoValueNHR04PUPPI+muPFIsoValuePhR04PUPPI)/pt", "muPFIsoValueCHR04PUPPI", "muPFIsoValueNHR04PUPPI","muPFIsoValuePhR04PUPPI","pt")
        process.TnP_MuonID.Cuts.puppiIsoCut =  cms.vstring("puppiIsoCut", "puppiIsoVar", "0.201")
    elif num == "puppiIsoNoLep":
        process.TnP_MuonID.Variables.pt = cms.vstring("pt", "0.0", "999", "")
        process.TnP_MuonID.Variables.muPFIsoValueCHR04PUPPINoLep = cms.vstring("muPFIsoValueCHR04PUPPINoLep", "-1.0", "99999999","")
        process.TnP_MuonID.Variables.muPFIsoValueNHR04PUPPINoLep = cms.vstring("muPFIsoValueNHR04PUPPINoLep","-1.0",  "99999999", "")
        process.TnP_MuonID.Variables.muPFIsoValuePhR04PUPPINoLep = cms.vstring("muPFIsoValuePhR04PUPPINoLep", "-1.0", "99999999", "")
        process.TnP_MuonID.Expressions.puppiIsoNoLepVar = cms.vstring("puppiIsoNoLepVar", "(muPFIsoValueCHR04PUPPINoLep+muPFIsoValueNHR04PUPPINoLep+muPFIsoValuePhR04PUPPINoLep)/pt", "muPFIsoValueCHR04PUPPINoLep", "muPFIsoValueNHR04PUPPINoLep","muPFIsoValuePhR04PUPPINoLep","pt")
        process.TnP_MuonID.Cuts.puppiIsoNoLepCut =  cms.vstring("puppiIsoNoLepCut", "puppiIsoNoLepVar", "0.123")
    elif num == "combpuppiIso":
        process.TnP_MuonID.Variables.pt = cms.vstring("pt", "0.0", "999", "")
        process.TnP_MuonID.Variables.muPFIsoValueCHR04PUPPI = cms.vstring("muPFIsoValueCHR04PUPPI", "-1.0", "99999999","")
        process.TnP_MuonID.Variables.muPFIsoValueNHR04PUPPI = cms.vstring("muPFIsoValueNHR04PUPPI","-1.0",  "99999999", "")
        process.TnP_MuonID.Variables.muPFIsoValuePhR04PUPPI = cms.vstring("muPFIsoValuePhR04PUPPI", "-1.0", "99999999", "")
        process.TnP_MuonID.Variables.muPFIsoValueCHR04PUPPINoLep = cms.vstring("muPFIsoValueCHR04PUPPINoLep", "-1.0", "99999999","")
        process.TnP_MuonID.Variables.muPFIsoValueNHR04PUPPINoLep = cms.vstring("muPFIsoValueNHR04PUPPINoLep","-1.0",  "99999999", "")
        process.TnP_MuonID.Variables.muPFIsoValuePhR04PUPPINoLep = cms.vstring("muPFIsoValuePhR04PUPPINoLep", "-1.0", "99999999", "")
        process.TnP_MuonID.Expressions.combpuppiIsoVar = cms.vstring("combpuppiIsoVar", "(muPFIsoValueCHR04PUPPINoLep+muPFIsoValueNHR04PUPPINoLep+muPFIsoValuePhR04PUPPINoLep+muPFIsoValueCHR04PUPPI+muPFIsoValueNHR04PUPPI+muPFIsoValuePhR04PUPPI)/(2*pt)", "muPFIsoValueCHR04PUPPINoLep", "muPFIsoValueNHR04PUPPINoLep","muPFIsoValuePhR04PUPPINoLep", "muPFIsoValueCHR04PUPPI", "muPFIsoValueNHR04PUPPI","muPFIsoValuePhR04PUPPI","pt")
        process.TnP_MuonID.Cuts.combpuppiIsoCut =  cms.vstring("combpuppiIsoCut", "combpuppiIsoVar", "0.15")
    elif num == "muCleanerIII":
        process.TnP_MuonID.Variables.numberOfMatchedStations  = cms.vstring("numberOfMatchedStations", "-0.5", "7.5", "")
        process.TnP_MuonID.Categories.TM = cms.vstring("TM", "dummy[pass=1,fail=0]")
        process.TnP_MuonID.Expressions.TM_cleanMuonIIIVar = cms.vstring("TM_cleanMuonIIIVar", "TM == 1 && numberOfMatchedStations > 0", "TM", "numberOfMatchedStations")
        process.TnP_MuonID.Cuts.TM_cleanMuonIIICut = cms.vstring("TM_cleanMuonIIICut", "TM_cleanMuonIIIVar", "0.5")    
    elif num == "muCleanerIV":
        process.TnP_MuonID.Variables.numberOfMatchedStations  = cms.vstring("numberOfMatchedStations", "-0.5", "7.5", "")
        process.TnP_MuonID.Variables.tkValidHits  = cms.vstring("tkValidHits", "-0.5", "1000", "") 
        process.TnP_MuonID.Variables.tkExpHitIn = cms.vstring("tkExpHitIn", "-0.5", "1000", "") 
        process.TnP_MuonID.Variables.tkHitFract  = cms.vstring("tkHitFract", "-0.5", "1000", "") 
        process.TnP_MuonID.Categories.TM = cms.vstring("Tracker Muon", "dummy[pass=1,fail=0]")
        process.TnP_MuonID.Expressions.TM_cleanMuonIVVar = cms.vstring("TM_cleanMuonIVVar", "TM == 1 && numberOfMatchedStations > 0 && (tkValidHits >= 10 || (tkValidHits >= 7 && tkHitFract==1))", "TM", "numberOfMatchedStations", "tkValidHits", "tkHitFract")
        process.TnP_MuonID.Cuts.TM_cleanMuonIVCut = cms.vstring("TM_cleanMuonIVCut", "TM_cleanMuonIVVar", "0.5")    
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
    if par == 'pt' or 'pt_eta':
        process.TnP_MuonID.Variables.pt  = cms.vstring("muon p_{T}", "0", "1000", "GeV/c")
    if par == 'pt_eta' or 'newpt_eta':
#        process.TnP_MuonID.Variables.abseta  = cms.vstring("muon |#eta|", "0", "2.5", "")
        process.TnP_MuonID.Variables.eta  = cms.vstring("muon #eta", "-1.2", "1.2", "")
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
    if par == 'newpt_eta':
        DEN.pair_newTuneP_probe_pt = cms.vdouble(10, 20, 25, 30, 40, 50, 60, 120) 
        DEN.eta = cms.vdouble(-1.2,-0.8,-0.5,-0.3,-0.2,0.0,0.2,0.3,0.5,0.8,1.2)
    elif par == 'newpt':
        DEN.pair_newTuneP_probe_pt = cms.vdouble(10, 20, 25, 30, 40, 50, 60, 120, 200)
    elif par == 'eta':
        DEN.eta = cms.vdouble(-2.4, -2.1, -1.6, -1.2, -0.9, -0.3, -0.2, 0.2, 0.3, 0.9, 1.2, 1.6, 2.1, 2.4)
    elif par == 'pt':
        DEN.pt = cms.vdouble(10, 20, 25, 30, 40, 50, 60, 120, 200)
#        DEN.pt = cms.vdouble(2.0, 2.5, 2.75, 3.0, 3.25, 3.5, 3.75, 4.0, 4.5, 5.0, 6.0, 8.0, 10.0, 15.0, 20.0, 25.0, 30.0, 40.0, 50.0, 60.0, 120.0, 200.0, 300.0, 500.0, 700.0, 1200.0)
    elif par == 'pair_deltaR':
        DEN.pair_deltaR = cms.vdouble(0., 0.4, 0.8, 1.2, 1.6, 2.0, 2.4, 2.8, 3.2, 5.0)
    elif par == 'tag_instLumi':
        DEN.tag_instLumi = cms.vdouble(1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600, 2800, 3000, 3200, 3400, 3600, 3800, 4000, 4200, 4400, 4600, 4800, 5000, 5200, 5400, 5600, 5800, 6000, 6200, 6400, 6600, 6800, 7000, 7200, 7400, 7600, 7800, 8000, 8200, 8400, 8600, 8800, 9000, 9200, 9400, 9600, 9800, 10000, 10200, 10400, 10600, 10800, 11000) # for runs BCD 
    elif par == 'pt_eta':
        DEN.pt = cms.vdouble(10, 20, 25, 30, 40, 50, 60, 120)
#        DEN.abseta = cms.vdouble( 0., 0.9, 1.2, 2.1, 2.4)
        DEN.eta = cms.vdouble(-1.2,-0.8,-0.5,-0.3,-0.2,0.0,0.2,0.3,0.5,0.8,1.2)
#        DEN.eta = cms.vdouble(-2.5,-2.4,-2.3,-2.2,-2.1,-2.0,-1.7,-1.6,-1.5,-1.4,-1.2,-0.8,-0.5,-0.3,-0.2,0.0,0.2, 0.3, 0.5, 0.8, 1.2, 1.4, 1.5, 1.6, 1.7, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5)
    elif par == 'vtx':
        print 'I filled it also asdf'
# first_single       DEN.tag_nVertices = cms.vdouble(10.5,14.5,18.5,22.5,26.5,30.5,34.5,50.5)
        DEN.tag_nVertices = cms.vdouble(6.5,10.5,14.5,18.5,22.5,26.5,30.5,34.5,50.5)


 #Selections
    if den == "gentrack": pass
    elif den == "looseid": DEN.PF = cms.vstring("pass")
    elif den == "mediumid": DEN.Medium = cms.vstring("pass")
    elif den == "tightid": 
        DEN.Tight2012 = cms.vstring("pass")
        DEN.dzPV = cms.vdouble(-0.5, 0.5)
    elif den == "tightidhww":
        DEN.Tight2012 = cms.vstring("pass")
        DEN.dzPV = cms.vdouble(-0.1, 0.1)
        DEN.dB = cms.vdouble(0.0, 0.02)
    elif den == "highptid":
        DEN.HighPt = cms.vstring("pass")
        DEN.dzPV = cms.vdouble(-0.5, 0.5)


args = sys.argv[1:]
iteration = ''
if len(args) > 1: iteration = args[1]
print "The iteration is", iteration
num = 'tight'
if len(args) > 2: num = args[2]
print 'The den is', num 
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
else:
    print 'Will use the standard fit functions for the backgroud'


process = cms.Process("TagProbe")
process.load('FWCore.MessageService.MessageLogger_cfi')
process.source = cms.Source("EmptySource")
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )

if not num  in ['looseid', 'mediumid', 'tightid', 'tightidhww', 'puppiIso', 'puppiIsoNoLep', 'combpuppiIso','muCleanerIII', 'muCleanerIV', 'highptid', 'looseiso', 'tightiso', 'tklooseiso']:
    print '@ERROR: num should be in ',['looseid', 'mediumid', 'tightid', 'tightidhww', 'puppiIso', 'puppiIsoNoLep', 'combpuppiIso', 'muCleanerIII', 'muCleanerIV', 'highptid', 'looseiso', 'tightiso', 'tklooseiso'], 'You used', num, '.Abort'
    sys.exit()
if not den in ['looseid', 'mediumid', 'tightid', 'tightidhww', 'highptid', 'gentrack']:
    print '@ERROR: den should be',['looseid', 'mediumid', 'tightid', 'tightidhww', 'highptid'], 'You used', den, '.Abort'
    sys.exit()
if not par in  ['pt', 'eta', 'vtx', 'pt_eta', 'newpt', 'newpt_eta', 'tag_instLumi', 'pair_deltaR']:
    print '@ERROR: par should be', ['pt', 'eta', 'vtx', 'pt_eta', 'newpt', 'newpt_eta', 'tag_instLumi', 'pair_deltaR'], 'You used', par, '.Abort'

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
                          SplitMode = cms.uint32(500000),
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



if sample == "dataid_BCDEF":                                                                                                                  
    process.TnP_MuonID = Template.clone(                                                                                                 
       InputFileNames = cms.vstring(                                                                                                    
            '/eos/cms/store/group/phys_muon/fernanpe/2016trees_rereco/TnPTreeZ_LegacyRereco07Aug17_SingleMuon_Run2016Bver2_GoldenJSON_skimmedID.root',
            '/eos/cms/store/group/phys_muon/fernanpe/2016trees_rereco/TnPTreeZ_LegacyRereco07Aug17_SingleMuon_Run2016C_GoldenJSON_skimmedID.root',
            '/eos/cms/store/group/phys_muon/fernanpe/2016trees_rereco/TnPTreeZ_LegacyRereco07Aug17_SingleMuon_Run2016D_GoldenJSON_skimmedID.root',
            '/eos/cms/store/group/phys_muon/fernanpe/2016trees_rereco/TnPTreeZ_LegacyRereco07Aug17_SingleMuon_Run2016E_GoldenJSON_skimmedID.root',
            '/eos/cms/store/group/phys_muon/fernanpe/2016trees_rereco/TnPTreeZ_LegacyRereco07Aug17_SingleMuon_Run2016F_GoldenJSON_skimmedID.root'
            ),                                                                                                                           
        InputTreeName = cms.string("fitter_tree"),                                                                                       
        InputDirectoryName = cms.string("tpTree"),                                                                                       
        OutputFileName = cms.string("TnP_MuonISO_%s.root" % scenario),                                                                   
        Efficiencies = cms.PSet(),                                                                                                       
        )  

if sample == "dataid_GH":     
    process.TnP_MuonID = Template.clone(                                                                                                 
       InputFileNames = cms.vstring(                                                                                                    
            '/eos/cms/store/group/phys_muon/fernanpe/2016trees_rereco/TnPTreeZ_LegacyRereco07Aug17_SingleMuon_Run2016G_GoldenJSON_skimmedID.root',
            '/eos/cms/store/group/phys_muon/fernanpe/2016trees_rereco/TnPTreeZ_LegacyRereco07Aug17_SingleMuon_Run2016H_GoldenJSON_skimmedID.root'
            ),                                                                                                                           
        InputTreeName = cms.string("fitter_tree"),                                                                                       
        InputDirectoryName = cms.string("tpTree"),                                                                                       
        OutputFileName = cms.string("TnP_MuonISO_%s.root" % scenario),                                                                   
        Efficiencies = cms.PSet(),                                                                                                       
        )  


if sample == "mcid_BCDEF":
    process.TnP_MuonID = Template.clone(                                                                                                 
       InputFileNames = cms.vstring(                            
            '/eos/cms/store/group/phys_muon/fernanpe/2016trees_rereco/MC_Moriond17_DY_tranch4Premix_skimmedID_weightedBCDEF.root'
            ),                                                                                                                           
        InputTreeName = cms.string("fitter_tree"),                                                                                       
        InputDirectoryName = cms.string("tpTree"),                                                                                       
        OutputFileName = cms.string("TnP_MuonISO_%s.root" % scenario),                                                                   
        Efficiencies = cms.PSet(),                                                                                                       
        )  

if sample == "mcid_GH":
    process.TnP_MuonID = Template.clone(                                                                                                 
       InputFileNames = cms.vstring(                            
            '/eos/cms/store/group/phys_muon/fernanpe/2016trees_rereco/MC_Moriond17_DY_tranch4Premix_skimmedID_weightedGH.root'
            ),                                                                                                                           
        InputTreeName = cms.string("fitter_tree"),                                                                                       
        InputDirectoryName = cms.string("tpTree"),                                                                                       
        OutputFileName = cms.string("TnP_MuonISO_%s.root" % scenario),                                                                   
        Efficiencies = cms.PSet(),                                                                                                       
        )  



if scenario == "mc_all":
    print "Including the weight for MC"
    process.TnP_MuonID.WeightVariable = cms.string("weight")
    process.TnP_MuonID.Variables.weight = cms.vstring("weight","0","10","")


BIN = cms.PSet(
        )

print 'debug1'
Num_dic = {'looseid':'LooseID','mediumid':'MediumID','tightid':'TightID','tightidhww':'TightIDHWW','puppiIso':'PuppiIso','puppiIsoNoLep':'PuppiIsoNoLep','combpuppiIso':'combPuppiIso', 'muCleanerIII':'MuonCleanerIII', 'muCleanerIV':'MuonCleanerIV', 'highptid':'HighPtID','looseiso':'LooseRelIso','tightiso':'TightRelIso','tklooseiso':'LooseRelTkIso'}
Den_dic = {'gentrack':'genTracks','looseid':'LooseID','mediumid':'MediumID','tightid':'TightIDandIPCut','tightidhww':'TightIDHWW','highptid':'HighPtIDandIPCut'}
Sel_dic = {'looseid':'Loose_noIP','mediumid':'Medium_noIP','tightid':'Tight2012_zIPCut','tightidhww':'Tight2012_zIPdBCut','puppiIso':'puppiIsoCut', 'puppiIsoNoLep':'puppiIsoNoLepCut','combpuppiIso':'combpuppiIsoCut','muCleanerIII':'TM_cleanMuonIIICut', 'muCleanerIV':'TM_cleanMuonIVCut', 'highptid':'HighPt_zIPCut','looseiso':'LooseIso4','tightiso':'TightIso4','tklooseiso':'LooseTkIso3'}

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
    module = process.TnP_MuonID.clone(OutputFileName = cms.string(_output + "/TnP_MC_%s.root" % (X)))
    #save the fitconfig in the plot directory
    shutil.copyfile(os.getcwd()+'/fitMuon2_part2.py',_output+'/fitMuon2_part2.py')
    shape = cms.vstring("vpvPlusExpo")
    print 'debug2'



    DEN = B.clone(); num_ = ID;
    FillBin(par)

    if not "iso" in num: #customize only for ID
        if bgFitFunction == 'default':
                if ('pt' in X):
                    print 'den is', den 
                    print 'num_ is ', num
                    if den == "highptid" or num == "highptid" or den == "trkhighptid" or num == "trkhighptid":
                        if (len(DEN.pair_newTuneP_probe_pt)==9 or len(DEN.pair_newTuneP_probe_pt)==8 or len(DEN.pair_newTuneP_probe_pt)==10):
                            shape = cms.vstring("vpvPlusCMS","*pt_bin0*","vpvPlusCMS","*pt_bin1*","vpvPlusCMS","*pt_bin2*","vpvPlusCMS","*pt_bin3*","vpvPlusCMSbeta0p2","*pt_bin4*","vpvPlusCMSbeta0p2","*pt_bin5*","vpvPlusCMSbeta0p2","*pt_bin6*","vpvPlusCMSbeta0p2","*pt_bin7*","vpvPlusCMSbeta0p2", "*pt_bin8*","vpvPlusCMSbeta0p2")
                        if scenario == "mc_all":
                            if (len(DEN.pair_newTuneP_probe_pt)==9 or len(DEN.pair_newTuneP_probe_pt)==8 or len(DEN.pair_newTuneP_probe_pt)==10):
                                shape = cms.vstring("vpvPlusCMSbeta0p2","*pt_bin0*","vpvPlusExpo","*pt_bin1*","vpvPlusExpo","*pt_bin2*","vpvPlusExpo","*pt_bin3*","vpvPlusExpo","*pt_bin4*","vpvPlusCMSbeta0p2","*pt_bin5*","vpvPlusCMSbeta0p2","*pt_bin6*","vpvPlusCMSbeta0p2","*pt_bin7*","vpvPlusCMSbeta0p2", "*pt_bin8*","vpvPlusCMSbeta0p2")

                    else:
                        if (len(DEN.pt)==26):
                            shape = cms.vstring("vpvPlusCMSbeta0p2")
                        if scenario == "mc_all":
                            shape = cms.vstring("vpvPlusCMSbeta0p2")

                        if (len(DEN.pt)==9 or len(DEN.pt)==8 or len(DEN.pt)==10):
                            shape = cms.vstring("vpvPlusCMS","*pt_bin0*","vpvPlusCMS","*pt_bin1*","vpvPlusCMS","*pt_bin2*","vpvPlusCMS","*pt_bin3*","vpvPlusCMSbeta0p2","*pt_bin4*","vpvPlusCMSbeta0p2","*pt_bin5*","vpvPlusCMSbeta0p2","*pt_bin6*","vpvPlusCMSbeta0p2","*pt_bin7*","vpvPlusCMSbeta0p2","*pt_bin8*","vpvPlusCMSbeta0p2")

        elif bgFitFunction == 'CMSshape':
            if den == "highpt":
                if (len(DEN.pair_newTuneP_probe_pt)==9):
                    shape = cms.vstring("vpvPlusExpo","*pt_bin4*","vpvPlusCMS","*pt_bin5*","vpvPlusCMS","*pt_bin6*","vpvPlusCheb","*pt_bin7*","vpvPlusCheb")
            else:
                if (len(DEN.pt)==9):
                    shape = cms.vstring("vpvPlusExpo","*pt_bin4*","vpvPlusCMS","*pt_bin5*","vpvPlusCheb","*pt_bin6*","vpvPlusCheb", "*pt_bin7*","vpvPlusCheb")



    print 'd3'
    mass_variable ="mass"
    print 'den is', den
    if den == "highptid" or den == "trkhighptid":
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
    elif scenario == 'mc_all' and par=='vtx':
        print 'MC sample as function of nVertices -> the PU reweighting will not be applied'
        if num_.find("Iso4") != -1 or num_.find("Iso3") != -1:
            setattr(module.Efficiencies, ID+"_"+X, cms.PSet(
                EfficiencyCategoryAndState = cms.vstring(num_,"below"),
                UnbinnedVariables = cms.vstring(mass_variable),
                BinnedVariables = DEN,
                BinToPDFmap = shape
                ))
        else:
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
    elif scenario == 'mc_all' and par!='vtx':
        # PU reweighting applied for MC when par != vtx
        print 'the PU reweighting will be applied'
        if num_.find("Iso4") != -1 or num_.find("Iso3") != -1:
            setattr(module.Efficiencies, ID+"_"+X, cms.PSet(
                EfficiencyCategoryAndState = cms.vstring(num_,"below"),
                UnbinnedVariables = cms.vstring(mass_variable, "weight"),
                BinnedVariables = DEN,
                BinToPDFmap = shape
                ))
        else:
            setattr(module.Efficiencies, ID+"_"+X, cms.PSet(
                EfficiencyCategoryAndState = cms.vstring(num_,"above"),
                UnbinnedVariables = cms.vstring(mass_variable, "weight"),
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
