#include "ds_evt.h"
#include <cmath>

ClassImp(ds_evt)

ds_evt::ds_evt(void) {
    Clear();
}

void ds_evt::Clear(void) {
    info.Clear();
    mode = -1; flv = 0;
    m = 0; p = 0; pcms = 0; costh = 0;
    mvec = 0;
    pvec = 0.;
    ptvec = 0.;
    cos_hel_vec = -2.;

    h_ds.Clear();
    ks_ds.Clear();

    h1_vec.Clear();
    h2_vec.Clear();

    ipbst.Clear();
}

double ds_evt::costhvec(void) const {
    double p[3];
    for (int i = 0; i < 3; i++)
        p[i] = h1_vec.p[i] + h2_vec.p[i];
    return p[2] / sqrt(p[0]*p[0] + p[1]*p[1]+ p[2]*p[2]);
}
