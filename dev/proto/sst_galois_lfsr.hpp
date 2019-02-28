#ifndef _sst_galois_lfsr_H
#define _sst_galois_lfsr_H

#include "sstscit.hpp"

#include <sst/core/component.h>
#include <sst/core/elementinfo.h>


class sst_galois_lfsr : public SST::Component {

public:

    sst_galois_lfsr(SST::ComponentId_t, SST::Params &);

    ~sst_galois_lfsr();

    void setup();

    void finish();

    bool tick(SST::Cycle_t);

    // Register the component
    SST_ELI_REGISTER_COMPONENT(
            sst_galois_lfsr, // class
            "sst_galois_lfsrSST", // element library
            "sst_galois_lfsr", // component
            SST_ELI_ELEMENT_VERSION(1, 0, 0),
            "Simple 4-bit Galois Linear Feedback Shift Register",
            COMPONENT_CATEGORY_UNCATEGORIZED
    )

private:

    // SST parameters
    SST::Output m_output;
    std::string m_proc;

};

#endif
