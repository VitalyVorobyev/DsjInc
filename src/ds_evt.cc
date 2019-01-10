#include "ds_evt.h"
#include <cmath>

ClassImp(ds_evt)

ds_evt::ds_evt(void) {
    Clear();
}

void ds_evt::Clear(void) {
    info.Clear();
    mode = -1; flv = 0; m = 0; mvec = 0;
    pvec[0] = -99; pvec[1] = -99; pvec[2] = -99;
    cos_hel_vec = -2.;

    h_ds.Clear();
    ks_ds.Clear();

    h1_vec.Clear();
    h2_vec.Clear();

    ipbst.Clear();
}

double ds_evt::Pvec(void) const {
    return sqrt(pvec[0]*pvec[0] + pvec[1]*pvec[1] + pvec[2]*pvec[2]);
}

double ds_evt::ptvec(void) const {
    return sqrt(pvec[0]*pvec[0] + pvec[1]*pvec[1]);
}

double ds_evt::costhvec(void) const {
    return pvec[2] / Pvec();
}

