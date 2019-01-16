#ifndef __DS_EVT_H__
#define __DS_EVT_H__

#include "TObject.h"
#include "mytools/datastructures.h"

class ds_evt : public TObject {
 public:
    ds_evt(void);
    void Clear(void);
    /// exp, run, evtn
    EvtInfo info;
    /// Ds meson decay mode
    /// 0 : Ds+ -> phi pi+
    /// 1 : Ds+ -> anti-K*0 K+, anti-K*0 -> K- pi+
    /// 2 : Ds+ -> Ks0 K+
    int mode;
    int flv;
    /// Ds+ mass
    double m;
    /// Ds+ momentum in the lab frame
    double p;
    /// Ds+ momentum in the CMS frame
    double pcms;
    /// cosine of the Ds+ polar angle in the lab frame
    double costh;
    /// phi or K*0 mass
    double mvec;
    /// phi or K*0 momentum
    double pvec;
    /// phi or K*0 transverse momentum
    double ptvec;

    /// polar angle of phi or K*0
    double costhvec(void) const;

    /// Helicity angle for phi of K*0
    double cos_hel_vec;

    //////////////////////
    // * Ds meson FSP * //
    //////////////////////
    /// K+ or pi+ from Ds+ -> phi pi+ or Ds+ -> Ks0 K+, K*0 K+
    TrackInfo h_ds;
    /// Ks0 from Ds+ -> Ks0 K+
    Ks0Info ks_ds;

    /////////////////////////
    // * phi and K*0 FSP * //
    /////////////////////////
    /// h1 from phi -> h1 h2 or K*0 -> h1 h2
    TrackInfo h1_vec;
    /// h2 from phi -> h1 h2 or K*0 -> h1 h2
    TrackInfo h2_vec;
    /// Beam interaction point and CMS boost vector
    IPBoost ipbst;

    ClassDef(ds_evt, 2)
};

#ifdef __MAKECINT__
#pragma link C++ class ds_evt;
#endif

#endif

