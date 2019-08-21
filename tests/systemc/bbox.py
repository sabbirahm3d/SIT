#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.getcwd()))
SCRIPT_PATH = os.path.join(BASE_DIR, "ssti", "boilerplate")
BBOX_DIR_PATH = os.path.join(BASE_DIR, "examples", "unit", "blackboxes")
DRVR_TEMPL_PATH = os.path.join(SCRIPT_PATH, "template", "driver.hpp")
MODEL_TEMPL_PATH = os.path.join(SCRIPT_PATH, "template", "model.hpp")
sys.path.append(SCRIPT_PATH)
from generate import BoilerPlate

if __name__ == "__main__":

    boilerplate_obj = BoilerPlate(
        module="ram",
        lib="systemc",
        ipc="sock",
        drvr_templ_path=DRVR_TEMPL_PATH,
        sst_model_templ_path=MODEL_TEMPL_PATH,
        desc="Demonstration of a SystemC hardware simulation in SST",
        link_desc={
            "link_desc0": "Traffic Light FSM data_in",
            "link_desc1": "Traffic Light FSM data_out",
        }
    )
    boilerplate_obj.set_ports((
        ("<sc_uint<ADDR_WIDTH> >", "address", "input"),
        ("<bool>", "cs", "input"),
        ("<bool>", "we", "input"),
        ("<bool>", "oe", "input"),
        ("<sc_uint<DATA_WIDTH> >", "data_in", "input"),
        ("<sc_uint<DATA_WIDTH> >", "data_out", "output"),

    ))
    boilerplate_obj.generate_bbox()
