/** Module for inclusive Dsj reconstruction
 *
 * Author: Vitaly Vorobyev (vvorob@inp.nsk.su)
 * Date: Sept 2018
 *
 **/

#include "belle.h"
#include "event/BelleEvent.h"
#include "particle/Particle.h"
#include "basf/module.h"

#include <vector>
#include <map>
#include <memory>
#include <string>

#include <TTree.h>
#include <TFile.h>

#include "dsjinc_evt.h"
#include "dsjinc_mcevt.h"
#include "ds_evt.h"
#include "ds_mcevt.h"

#if defined(BELLE_NAMESPACE)
namespace Belle {
#endif

class dsjinc : public Module {
    int makeDs(double minP);
    int makeDsj(void);

    dsjinc_evt* evt;
    ds_evt* dsevt;
    dsjinc_mcevt* mcevt;
    ds_mcevt* dsmcevt;

    bool IsMC(void);
    bool mc_flag;
    TTree* dsjTree;
    TTree* dsTree;
    TFile* tfile;
    int clock;
    void begin_event(BelleEvent* evptr);

    std::map<std::string, std::vector<Particle>> plm;

    void DumpEvent(void);
    void FillEvt(Particle& dsj);
    void FillDsEvt(Particle& ds);

    void FillVec(const Particle& vec);
    void record(std::vector<Particle>& v);
    void recordDs(std::vector<Particle>& v);

 public:
    dsjinc(void) : clock(0), ntuple_flag(1), m_mode(0), min_ds_mom(1.5) {}
    ~dsjinc(void) = default;
    void init(int *);
    void term(void);
    void disp_stat(const char*){}
    void hist_def(void) {}
    void begin_run(BelleEvent*, int*);
    void event(BelleEvent*, int*);
    void end_run(BelleEvent*, int*){}

    int ntuple_flag;
    int m_mode; // 0 -> Data
                // 1 -> Signal MC
                // 2 -> Genegic M
    char ofile[1024];
    double min_ds_mom;
};

#if defined(BELLE_NAMESPACE)
}
#endif

