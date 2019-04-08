#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import SystemRandom
from string import ascii_uppercase, digits
import os

import sst

BASE_PATH = os.getcwd()
CLOCK = "1MHz"
sst.setProgramOption("stopAtCycle", "100us")

# Component proto from element proto (proto.proto), named "Main Car Wash"
carWashComponent = sst.Component("Main Car Wash", "proto.proto")
carWashComponent.addParams({
    "simulationTime": "24",  # simulate 24 hours
    "tickFreq": CLOCK,  # process cars every 60 seconds (1 tick = 1 minute)
})

# Subcomponent slot "bay" using component bay from element proto (proto.bay), number 0
baySubcomponent0 = carWashComponent.setSubComponent("bay", "proto.bay", 0)
baySubcomponent0.addParams({
    "size": "1",  # small car bay
    "smallCarWashTime": "3"
})

# Subcomponent slot "bay" using component bay from element proto (proto.bay), number 1
baySubcomponent1 = carWashComponent.setSubComponent("bay", "proto.bay", 1)
baySubcomponent1.addParams({
    "size": "2",  # large car bay
    "smallCarWashTime": "3",
    "largeCarWashTime": "5"
})

# Subcomponent slot "bay" using component bay from element proto (proto.bay), number 2
baySubcomponent2 = carWashComponent.setSubComponent("bay", "proto.bay", 2)
baySubcomponent2.addParams({
    "size": "2",  # large car bay
    "smallCarWashTime": "3",
    "largeCarWashTime": "5"
})

# Component carGenerator from element proto (proto.carGenerator), named "Car Generator"
carGeneratorComponent = sst.Component("Car Generator", "proto.car_generator")
carGeneratorComponent.addParams({
    "delay": CLOCK,  # send a car every 60 seconds (1 tick = 1 minute)
})

# Connect the proto and carGenerator components
sst.Link("MyLink").connect(
    (carWashComponent, "port", "1ps"),
    (carGeneratorComponent, "port", "1ps")
)



galois_lfsr_comp = sst.Component("galois_lfsr", "proto.galois_lfsr")
# override default parameters
galois_lfsr_comp.addParams({
    "proc": os.path.join(BASE_PATH, "galois_lfsr.o"),
    "ipc_port": "/tmp/" + ''.join(SystemRandom().choice(ascii_uppercase + digits) for _ in range(8)),
    "clock": CLOCK,
})

fib_lfsr_comp = sst.Component("fib_lfsr", "proto.fib_lfsr")
# override default parameters
fib_lfsr_comp.addParams({
    "proc": os.path.join(BASE_PATH, "fib_lfsr.o"),
    "ipc_port": "/tmp/" + ''.join(SystemRandom().choice(ascii_uppercase + digits) for _ in range(8)),
    "clock": CLOCK,
})

sst.Link("galois_lfsr_din").connect(
    (galois_lfsr_comp, "galois_lfsr_din", "1ps"),
    (carGeneratorComponent, "galois_lfsr_din", "1ps"),
)
sst.Link("galois_lfsr_dout").connect(
    (galois_lfsr_comp, "galois_lfsr_dout", "1ps"),
    (carGeneratorComponent, "galois_lfsr_dout", "1ps"),
)

sst.Link("fib_lfsr_din").connect(
    (fib_lfsr_comp, "fib_lfsr_din", "1ps"),
    (carGeneratorComponent, "fib_lfsr_din", "1ps"),
)
sst.Link("fib_lfsr_dout").connect(
    (fib_lfsr_comp, "fib_lfsr_dout", "1ps"),
    (carGeneratorComponent, "fib_lfsr_dout", "1ps"),
)
