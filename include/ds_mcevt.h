#ifndef __DS_MCEVT_H__
#define __DS_MCEVT_H__

#include "TObject.h"
#include "mytools/datastructures.h"

class ds_mcevt : public TObject {
 public:
    ds_mcevt(void);
    void Clear(void);
    /// Signal event
    bool Sig(void) const;
    /// Combinatorial bkg
    bool Cmb(void) const;
    /// Non-combinatorial bkg
    bool Bkg(void) const;

    GenHepEvt genhep;

    GenParticleInfo ds_gen;
    GenParticleInfo h_ds_gen;
    GenParticleInfo ks_ds_gen;
    GenParticleInfo h1_vec_gen;
    GenParticleInfo h2_vec_gen;

    ClassDef(ds_mcevt, 1)
};

#ifdef __MAKECINT__
#pragma link C++ class ds_mcevt;
#endif

#endif

