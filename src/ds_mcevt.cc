#include "ds_mcevt.h"
#include <cmath>

ClassImp(ds_mcevt)

ds_mcevt::ds_mcevt(void) {
    Clear();
}

void ds_mcevt::Clear(void) {
    ds_gen.Clear();

    h_ds_gen.Clear();
    ks_ds_gen.Clear();

    h1_vec_gen.Clear();
    h2_vec_gen.Clear(); 
}

bool ds_mcevt::Sig(void) const {
    return (ds_gen.flag == 1 || ds_gen.flag == 5 || ds_gen.flag == 10);
}
/// Combinatorial bkg
bool ds_mcevt::Cmb(void) const {
    return ds_gen.flag == -1;
}
/// Non-combinatorial bkg
bool ds_mcevt::Bkg(void) const {
    return !Sig() && !Cmb();
}

