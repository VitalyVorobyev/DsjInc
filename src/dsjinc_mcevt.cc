#include "dsjinc_mcevt.h"
#include <cmath>

ClassImp(dsjinc_mcevt)

dsjinc_mcevt::dsjinc_mcevt(void) {
    Clear();
}

void dsjinc_mcevt::Clear(void) {
    dsj_gen.Clear();
    ds_gen.Clear();

    gam_dsst_gen.Clear();

    gam_dsj_gen.Clear();
    pi0_dsj_gen.Clear();
    pip_dsj_gen.Clear();
    pim_dsj_gen.Clear();

    h_ds_gen.Clear();
    ks_ds_gen.Clear();

    h1_vec_gen.Clear();
    h2_vec_gen.Clear(); 
}

bool dsjinc_mcevt::Sig(void) const{
    return (dsj_gen.flag == 1 || dsj_gen.flag == 5 || dsj_gen.flag == 10);
}
/// Combinatorial bkg
bool dsjinc_mcevt::Cmb(void) const{
    return dsj_gen.flag == -1;
}
/// Non-combinatorial bkg
bool dsjinc_mcevt::Bkg(void) const{
    return !Sig() && !Cmb();
}

