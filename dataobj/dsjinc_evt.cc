#include "dsjinc_evt.h"
#include <cmath>

ClassImp(dsjinc_evt)

dsjinc_evt::dsjinc_evt(void) {
    Clear();
}

void dsjinc_evt::Clear(void) {
    info.Clear();
    mode_ds = -1; mode = -1; flv = 0;
    m = 0; mds = 0; pcmsds = 0; dmdsst = 0; mvec = 0;
    cos_hel_dsj = -2.; cos_hel_vec = -2.;
    mchildren = 0.;

    gam_dsj.Clear();
    gam_dsst.Clear();
    pi0_dsj.Clear();
    pi0lo_dsj.Clear();
    pip_dsj.Clear();
    pim_dsj.Clear();
}
