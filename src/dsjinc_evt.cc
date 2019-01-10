#include "dsjinc_evt.h"
#include <cmath>

ClassImp(dsjinc_evt)

dsjinc_evt::dsjinc_evt(void) {
    Clear();
}

void dsjinc_evt::Clear(void) {
    info.Clear();
    mode_ds = -1; mode = -1; flv = 0;
    m = 0; mds = 0; dmdsst = 0; mvec = 0;
    cos_hel_dsj = -2.; cos_hel_vec = -2.;

    gam_dsj.Clear();
    gam_dsst.Clear();
    pi0_dsj.Clear();
    pip_dsj.Clear();
    pim_dsj.Clear();
}

bool dsjinc_evt::DsstFl(void) const {
    return (mode > 0) && (mode / 10);
}

bool dsjinc_evt::DsjPi0Fl(void) const {
    return (mode > 0) && ((mode % 10) == 1);
}

bool dsjinc_evt::DsjGammaFl(void) const {
    return (mode > 0) && ((mode % 10) == 0);
}

