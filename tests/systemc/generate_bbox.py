#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
SCRIPT_PATH = os.path.join(BASE_DIR, "ssti")
sys.path.append(SCRIPT_PATH)
from boilerplate import SystemC

if __name__ == "__main__":

    ARGS = dict(
        module_dir="../../common/",
        ports_dir="../../common/blackboxes/",
        lib_dir="../../../../ssti/",
        module="ram",
        lib="tests",
        desc="Demonstration of a SystemC hardware simulation in SST",
        link_desc={
            "link_desc0": "RAM data_in",
            "link_desc1": "RAM data_out",
        }
    )

    boilerplate_obj = SystemC(**ARGS, ipc=sys.argv[-1])
    boilerplate_obj.set_ports((
        ("<sc_bv<ADDR_WIDTH>>//8", "address", "input"),
        ("<bool>", "cs", "input"),
        ("<bool>", "we", "input"),
        ("<bool>", "oe", "input"),
        ("<sc_bv<DATA_WIDTH>>//8", "data_in", "input"),
        ("<sc_bv<DATA_WIDTH>>//8", "data_out", "output"),
    ))
    boilerplate_obj.generate_bbox()
