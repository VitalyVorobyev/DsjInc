#include "dsjinc.h"

#include "particle/utility.h"
#include "basf/module_descr.h"
#include "ip/IpProfile.h"
#include "benergy/BeamEnergy.h"

#include "mytools/recotools.h"
#include "mytools/uisetter.h"
#include "mytools/combinator.h"
#include "mytools/geninfo.h"

#include <iostream>

const bool dump = false;

using std::cout;
using std::endl;
using std::cerr;

#if defined(BELLE_NAMESPACE)
namespace Belle {
#endif

typedef std::vector<Particle> PVec;

extern "C" Module_descr *mdcl_dsjinc() {
    dsjinc *module = new dsjinc;
    Module_descr *dscr = new Module_descr("dsjinc", module);
    BeamEnergy::define_global(dscr);
    dscr->define_param("mode", "mode", &module->m_mode);
    dscr->define_param("ofile", "ofile", 1024, module->ofile);
    dscr->define_param("ntuple_flag", "ntuple_flag", &module->ntuple_flag);
    dscr->define_param("min_ds_mom", "min_ds_mom", &module->min_ds_mom);
    return dscr;
}

void dsjinc::init(int *) {
    cout << "init" << endl;
    Combinator::init();
    Combinator::SetNT(ntuple_flag);
    Ptype dummy("VPHO");
}

bool dsjinc::IsMC(void) {
    Belle_runhead_Manager &rhd_mgr = Belle_runhead_Manager::get_manager();
    std::vector<Belle_runhead>::const_iterator rhd = rhd_mgr.begin();
    if (rhd == rhd_mgr.end()) {
        cerr << "Constructor: Cannot access to Belle_runhead" << endl;
        return false;
    }
    return rhd->ExpMC() != 1;
}

void dsjinc::begin_run(BelleEvent* evptr, int *status) {
    IpProfile::begin_run();
    BeamEnergy::begin_run();
    eid::init_data();
    mc_flag = IsMC();
    if (ntuple_flag && !clock) {
        clock = 1;
        tfile   = new TFile(ofile, "RECREATE");
        dsjTree = new TTree("dsj", "dsj");
        dsTree  = new TTree("ds", "ds");
        evt     = new dsjinc_evt();
        dsevt   = new ds_evt();
        cout << ofile << endl;
        dsjTree->Branch("evt", evt);
        dsTree->Branch("evt", dsevt);
        if (m_mode) {
            mcevt   = new dsjinc_mcevt();
            dsmcevt = new ds_mcevt();
            dsjTree->Branch("mcevt", mcevt);
            dsTree->Branch("mcevt", dsmcevt);
        }
        cout << "TTree tevt is initialized" << endl
             << " Ds momentum cut: " << min_ds_mom << endl;
    }
    Combinator::SetMC(mc_flag);
    UISetter::SetMC(mc_flag);
}

void dsjinc::term(void) {
    cout << "Term " << ofile << endl;
    if (ntuple_flag) {
        cout << " -> dsj: " << dsjTree->GetEntries() << endl
             << " ->  ds: " << dsTree->GetEntries() << endl;
        dsjTree->Write();
        dsTree->Write();
        tfile->Close();
    }
}

void dsjinc::begin_event(BelleEvent* evptr) {
    plm.clear();
    Belle_event_Manager& evtmgr = Belle_event_Manager::get_manager();
    Belle_event& evthead = *evtmgr.begin();
    const int evtn = evthead.EvtNo() & 0xfffffff;
    if (!(evtn % 100))
        cout << "run: " << evthead.RunNo() << ", evtn: " << evtn << endl;
    if (!IpProfile::usable())
        cout << "IP profile is not available!!! " << endl;
}

void dsjinc::event(BelleEvent* evptr, int *status) {
    *status = 0;
    begin_event(evptr);
    if (!makeDs(min_ds_mom))
        return;

    if (!ntuple_flag) {
        *status = 1;
        return;
    }

    recordDs(plm["Ds+"]);
    recordDs(plm["Ds-"]);

    makeDsj();
    record(plm["Dsj+"]);
    record(plm["Dsj-"]);
}

int dsjinc::makeDs(double minP) {
    Combinator::make_dstophipi(plm, 0);  // Ds+ -> phi pi+ (mode 0)
    Combinator::make_dstokstk( plm, 1);  // Ds+ -> K*0 K+  (mode 1)
    Combinator::make_dstoks0k( plm, 2);  // Ds+ -> Ks0 K+  (mode 2)
    withPSCut(plm["Ds+"], minP);
    withPSCut(plm["Ds-"], minP);
    return plm["Ds+"].size() + plm["Ds-"].size();
}

int dsjinc::makeDsj(void) {
    Combinator::make_dsjtodsgamma(    plm,  0);  // Dsj -> Ds gamma
    Combinator::make_dsjtodspi0(      plm,  1);  // Dsj -> Ds pi0
    Combinator::make_dsjtodspipi(     plm,  2);  // Dsj -> Ds pi+ pi-
    Combinator::make_dsjtods2pi0(     plm,  3);  // Dsj -> Ds pi0 pi0
    Combinator::make_dsjtods2gamma(   plm, 10);  // Dsj -> Ds gamma gamma
    Combinator::make_dsjtodspi0gamma( plm, 11);  // Dsj -> Ds pi0 gamma
    Combinator::make_dsjtodspipigamma(plm, 12);  // Dsj -> Ds pi+ pi- gamma
    Combinator::make_dsjtods2pi0gamma(plm, 13);  // Dsj -> Ds pi0 pi0 gamma

//    Combinator::make_dsjtodsstgamma(plm, 10);  // Dsj -> Ds* gamma
//    Combinator::make_dsjtodsstpi0(plm, 11);    // Dsj -> Ds* pi0
//    Combinator::make_dsjtodsstpipi(plm, 12);   // Dsj -> Ds* pi+ pi-
//    Combinator::make_dsjtodsstpi0pi0(plm, 13); // Dsj -> Ds* pi0 pi0
    return plm["Dsj+"].size() + plm["Dsj-"].size();
}

void dsjinc::DumpEvent(void) {
  cout << "Ds+: " << plm["Ds+"].size() << ", Ds-: " << plm["Ds-"].size() << endl
       << "pi0: " << plm["pi0"].size() << ", gamma: " << plm["gamma"].size() << endl
       << "    Ds*+: " << plm["Ds*+"].size() << endl
       << "    Ds*-: " << plm["Ds*-"].size() << endl
       << "    Dsj+: " << plm["Dsj+"].size() << endl
       << "    Dsj-: " << plm["Dsj-"].size() << endl;
}

void dsjinc::record(std::vector<Particle>& v) {
    for (auto it = v.begin(); it != v.end(); it++) { 
        evt->Clear();
        if (m_mode) mcevt->Clear();
        FillEvt(*it);
        dsjTree->Fill();
    }
}

void dsjinc::recordDs(std::vector<Particle>& v) {
    for (auto it = v.begin(); it != v.end(); it++) { 
        dsevt->Clear();
        if (m_mode) dsmcevt->Clear();
        FillDsEvt(*it);
        dsTree->Fill();
    }
}

void dsjinc::FillDsEvt(Particle& ds) {
    RTools::FillEvtInfo(dsevt->info);
    RTools::FillIPBoost(dsevt->ipbst);

    if (m_mode) {  // MC
        RTools::FillGenHepEvt(dsmcevt->genhep, 100);
        setMCtruth(ds);
        RTools::FillGenPInfo(ds, dsmcevt->ds_gen);
    }

    const DUserInfo& dsinfo = static_cast<DUserInfo&>(ds.userInfo());
    dsevt->mode  = dsinfo.Mode();
    dsevt->m     = ds.p().m();
    dsevt->p     = ds.p().rho();
    dsevt->costh = ds.p().cosTheta();
    dsevt->pcms  = pStar(ds.p()).rho();
    dsevt->flv   = ds.lund() > 0 ? 1 : -1;

    RTools::FillTrk(ds.child(1), dsevt->h_ds);
    if (m_mode) {
        RTools::FillGenPInfo(ds.child(0), dsmcevt->ks_ds_gen);
        RTools::FillGenPInfo(ds.child(1), dsmcevt->h_ds_gen);
    }
    switch (dsevt->mode) {
    case 0:  // Ds+ -> phi pi+
        FillVec(ds.child(0));
        break;
    case 1:  // Ds+ -> K*0 K+
        FillVec(ds.child(0));
        break;
    case 2:  // Ds+ -> Ks0 K+
        RTools::FillKs0(ds.child(0), dsevt->ks_ds);
        break;
    default:
        cerr << "dsjinc::FillDsEvt: unknown Ds meson decay: " << dsevt->mode << endl;
        break;
    }
}

void dsjinc::FillEvt(Particle& dsj) {
    RTools::FillEvtInfo(evt->info);
    if (m_mode) {
        setMCtruth(dsj);
        RTools::FillGenPInfo(dsj, mcevt->dsj_gen);
    }

    const DUserInfo& dsjinfo = static_cast<DUserInfo&>(dsj.userInfo());
    evt->mode = dsjinfo.Mode();
    evt->m    = dsj.p().m();
    evt->cos_hel_dsj = RTools::Helicity(dsj);

    const bool inv = (evt->mode == 3) || (evt->mode == 10) || (evt->mode == 13);

//    cout << "mode " << evt->mode << ": " << endl;
//    for (int i = 0; i < dsj.nChildren(); i++)
//        cout << "  " << i << ": " << dsj.child(i).lund() << " " << dsj.child(i).p().e() << endl;
//    cout << endl;

    switch (evt->mode % 10) {
    case 0: {  // Dsj* -> X gamma
        int idx = 1;
        if (inv) idx = dsj.child(0).p().e() > dsj.child(1).p().e() ? 1 : 0;
        const Particle& gamma = dsj.child(idx);
        RTools::FillGamma(gamma, evt->gam_dsj);
        if (m_mode) RTools::FillGenPInfo(gamma, mcevt->gam_dsj_gen);
        break;}
    case 1: {  // Dsj* -> X pi0
        const Particle& pi0 = dsj.child(1);
        RTools::FillPi0(pi0, evt->pi0_dsj);
        if (m_mode) RTools::FillGenPInfo(pi0, mcevt->pi0_dsj_gen);
        break; }
    case 2: {  // Dsj* -> X pi+ pi-
        const Particle& pip = dsj.child(1);
        const Particle& pim = dsj.child(2);
        RTools::FillTrk(pip, evt->pip_dsj);
        RTools::FillTrk(pim, evt->pim_dsj);
        if (m_mode) {
            RTools::FillGenPInfo(pip, mcevt->pip_dsj_gen);
            RTools::FillGenPInfo(pim, mcevt->pim_dsj_gen);
        }
        break; }
    case 3: { // Dsj* -> X pi0 pi0
        const Particle& pi01 = dsj.child(0);
        const Particle& pi02 = dsj.child(1);
//        if ((pi01.lund() != 111) || (pi02.lund() != 111)) {
//            cerr << "pi0 " << pi01.lund() << ", pi0 " << pi02.lund()
//                 << ", mode " << dsjinfo.Mode() << endl;
//            throw 2;
//        }
        RTools::FillPi0(pi01, evt->pi0_dsj);
        RTools::FillPi0(pi02, evt->pi0lo_dsj);
        if (m_mode) {
            RTools::FillGenPInfo(pi01, mcevt->pi0_dsj_gen);
            RTools::FillGenPInfo(pi02, mcevt->pi0lo_dsj_gen);
        }
        break; }
    default:
        cerr << "dsjinc::FillEvt: unknown Dsj mode " << evt->mode << endl;
        break;
    }

    //    const Particle& Ds = evt->DsstFl() ? dsj.child(0).child(0) : dsj.child(0);
    const Particle& Ds = dsj.child(inv ? 2 : 0);
    if (abs(Ds.lund()) != 431) {
        cerr << "Ds lund is " << Ds.lund() << ", Dsj mode " << dsjinfo.Mode() << endl;
        throw 1;
    }
    const DUserInfo& dsinfo = static_cast<const DUserInfo&>(Ds.userInfo());
    if (m_mode) RTools::FillGenPInfo(Ds, mcevt->ds_gen);
    evt->mode_ds = dsinfo.Mode();
    evt->mds     = Ds.p().m();
    evt->pcmsds  = pStar(Ds.p()).rho();
    evt->mvec    = Ds.child(0).p().m();
    evt->cos_hel_vec = RTools::Helicity(Ds);

    if (evt->mode / 10) {
        // A mode with additional photon
        int idx = dsj.nChildren() - 1;
        if (evt->mode == 10) idx = dsj.child(0).p().e() > dsj.child(1).p().e() ? 0 : 1;
        const Particle& gamma = dsj.child(idx);
        RTools::FillGamma(gamma, evt->gam_dsst);
        if(m_mode) RTools::FillGenPInfo(gamma, mcevt->gam_dsst_gen);
        const HepLorentzVector pdsst = Ds.p() + gamma.p();
        evt->dmdsst = pdsst.m() - Ds.p().m();
    }
}

void dsjinc::FillVec(const Particle& vec) {
    RTools::FillTrk(vec.child(0), dsevt->h1_vec);
    RTools::FillTrk(vec.child(1), dsevt->h2_vec);
    dsevt->mvec = vec.p().m();
    dsevt->cos_hel_vec = RTools::Helicity(vec);
    dsevt->pvec = vec.p().rho();
    dsevt->ptvec = vec.p().perp();
    if (m_mode) {
        RTools::FillGenPInfo(vec.child(0), dsmcevt->h1_vec_gen);
        RTools::FillGenPInfo(vec.child(1), dsmcevt->h2_vec_gen);
    }
}

#if defined(BELLE_NAMESPACE)
}
#endif

