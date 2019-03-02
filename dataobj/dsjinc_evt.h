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
    /// 00 : D*sj+ -> Ds+ gamma
    /// 01 : D*sj+ -> Ds+ pi0
    /// 02 : D*sj+ -> Ds+ pi+ pi-
    /// 03 : D*sj+ -> Ds+ pi0 pi0
    /// 10 : D*sj+ -> Ds+ gamma   gamma
    /// 11 : D*sj+ -> Ds+ pi0     gamma
    /// 12 : D*sj+ -> Ds+ pi+ pi- gamma
    /// 13 : D*sj+ -> Ds+ pi0 pi0 gamma
    int mode;
    int flv;
    /// D*sj mass
    double m;
    /// Ds+ mass
    double mds;
    /// Ds+ CMS momentum
    double pcmsds;
    /// D*s+ mass difference
    double dmdsst;
    /// phi or K*0 mass
    double mvec;
    /// Helicity angle for Dsj -> Ds X
    double cos_hel_dsj;
    /// Helicity angle for phi of K*0
    double cos_hel_vec;
    /// m(pi+ pi-), m(gamma gamma) or m(pi+ pi-)
    double mchildren;

    ////////////////////////
    // * Dsj mesons FSP * //
    ////////////////////////
    /// Photon from D*sj -> D(*)s gamma
    GammaInfo gam_dsj;
    /// Photon from D*s -> Ds gamma (gamma with smaller energy)
    GammaInfo gam_dsst;
    /// pi0 from D*sj -> D(*)s pi0 (pi0)
    Pi0Info pi0_dsj;
    /// Lower energy pi0 from D*sj -> D(*)s pi0 pi0
    Pi0Info pi0lo_dsj;
    /// pi+ from D*sj -> D(*)s pi+ pi-
    TrackInfo pip_dsj;
    /// pi- from D*sj -> D(*)s pi+ pi-
    TrackInfo pim_dsj;

    ClassDef(dsjinc_evt, 2)
};

#ifdef __MAKECINT__
#pragma link C++ class dsjinc_evt;
#endif

#endif

