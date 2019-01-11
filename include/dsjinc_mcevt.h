#ifndef __B2DDSJ_MCEVT_H__
#define __B2DDSJ_MCEVT_H__

#include "TObject.h"
#include "mytools/datastructures.h"

class dsjinc_mcevt : public TObject {
 public:
    dsjinc_mcevt(void);
    void Clear(void);

    /// Signal event
    bool Sig(void) const;
    /// Combinatorial bkg
    bool Cmb(void) const;
    /// Non-combinatorial bkg
    bool Bkg(void) const;

    GenParticleInfo dsj_gen;
    GenParticleInfo ds_gen;

    /// photon from Ds*
    GenParticleInfo gam_dsst_gen;

    // Dsj final-state particles
    GenParticleInfo gam_dsj_gen;
    GenParticleInfo pi0_dsj_gen;
    GenParticleInfo pi0lo_dsj_gen;
    GenParticleInfo pip_dsj_gen;
    GenParticleInfo pim_dsj_gen;

    // Ds final-state particles
    GenParticleInfo h_ds_gen;
    GenParticleInfo ks_ds_gen;

    // K*0 or phi final-state particles
    GenParticleInfo h1_vec_gen;
    GenParticleInfo h2_vec_gen;

    ClassDef(dsjinc_mcevt, 2)
};

#ifdef __MAKECINT__
#pragma link C++ class dsjinc_mcevt;
#endif

#endif

