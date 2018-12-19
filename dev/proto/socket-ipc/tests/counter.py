import os

import sst

# component counter from element counterSST (counterSST.counter) named "counter World"
counterComponent = sst.Component("sst_counter", "sst_counterSST.sst_counter")
sst.setProgramOption("stopAtCycle", "110ns")
# overide default parameters
counterComponent.addParams({
    "sysc_counter": os.path.join(os.environ["SYSC_KERNEL"], "examples", "sysc", "counter", "counter"),  # path to the SystemC executable
    "port": "8080"  # socket port number
})
