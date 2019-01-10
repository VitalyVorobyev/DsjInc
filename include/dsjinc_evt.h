#ifndef __DSJINC_EVT_H__
#define __DSJINC_EVT_H__

#include "TObject.h"
#include "mytools/datastructures.h"

class dsjinc_evt : public TObject {
 public:
    dsjinc_evt(void);
    void Clear(void);
    /// exp, run, evtn
    EvtInfo info;
    /// Ds meson decay mode
    /// 0 : Ds+ -> phi pi+
    /// 1 : Ds+ -> anti-K*0 K+, anti-K*0 -> K- pi+
    /// 2 : Ds+ -> Ks0 K+
    int mode_ds;
    /// D*sj meson decay mode
    /// 00 : D*sj+ -> Ds+  gamma
    /// 01 : D*sj+ -> Ds+  pi0
    /// 02 : D*sj+ -> Ds+  pi+ pi-
    /// 10 : D*sj+ -> D*s+ gamma
    /// 11 : D*sj+ -> D*s+ pi0
    /// 12 : D*sj+ -> D*s+ pi+ pi-
    int mode;
    int flv;
    bool DsstFl(void) const;
    bool DsjPi0Fl(void) const;
    bool DsjGammaFl(void) const;
    /// D*sj mass
    double m;
    /// Ds+ mass
    double mds;
    /// D*s+ mass difference
    double dmdsst;
    /// phi or K*0 mass
    double mvec;
    /// Helicity angle for Dsj -> Ds X
    double cos_hel_dsj;
    /// Helicity angle for phi of K*0
    double cos_hel_vec;

    ////////////////////////
    // * Dsj mesons FSP * //
    ////////////////////////
    /// Photon from D*sj -> D(*)s gamma
    GammaInfo gam_dsj;
    /// Photon from D*s -> Ds gamma
    GammaInfo gam_dsst;
    /// pi0 from D*sj -> D(*)s pi0
    Pi0Info pi0_dsj;
    /// pi+ from D*- -> D0 pi-
    TrackInfo pi_dst;
    /// pi+ from D*sj -> D(*)s pi+ pi-
    TrackInfo pip_dsj;
    /// pi- from D*sj -> D(*)s pi+ pi-
    TrackInfo pim_dsj;

    ClassDef(dsjinc_evt, 1)
};

#ifdef __MAKECINT__
#pragma link C++ class dsjinc_evt;
#endif

#endif

