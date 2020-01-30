#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import random
import sys

POPULATION_TOTAL = 7760000000
POPULATION_HEALTHY = POPULATION_TOTAL
CURE = 0.00
TIME = 0

while POPULATION_HEALTHY > 0 and CURE < 100:

    if TIME == 0:

        SEED = int(sys.argv[-1])
        random.seed(SEED)
        LIMIT = random.randint(3, 1000)

        POPULATION_INFECTED = 0
        TOTAL_INFECTED = 0
        POPULATION_DEAD = 0
        TOTAL_DEAD = 0
        POPULATION_AFFECTED = 0

        BIRTH_RATE = random.randint(2, LIMIT)
        BIRTH_RATE = 1 / BIRTH_RATE

        SEVERITY = random.randint(2, LIMIT)
        SEVERITY = 1 / SEVERITY  # rate of detection

        LETHALITY = random.randint(2, LIMIT)
        LETHALITY = 1 / LETHALITY  # rate of death

        INFECTIVITY = random.randint(2, LIMIT)
        INFECTIVITY = 1 / INFECTIVITY  # rate of infection

        CURE_THRESHOLD = POPULATION_TOTAL * SEVERITY
        CURE_THRESHOLD = CURE_THRESHOLD * BIRTH_RATE
        CURE_THRESHOLD = math.ceil(CURE_THRESHOLD)

    else:

        _INFECTIVITY = random.randint(2, LIMIT)
        _INFECTIVITY = 1 / _INFECTIVITY
        INFECTIVITY = INFECTIVITY + _INFECTIVITY
        INFECTIVITY = min(INFECTIVITY, 0.99)

        _LETHALITY = random.randint(2, LIMIT)
        _LETHALITY = 1 / _LETHALITY
        LETHALITY = LETHALITY + _LETHALITY
        LETHALITY = min(LETHALITY, 0.99)

        if TOTAL_INFECTED > CURE_THRESHOLD:

            RESEARCH = random.randint(2, LIMIT)
            RESEARCH = 1 / RESEARCH
            CURE = CURE + RESEARCH

            MUTATED_GENE = random.randint(0, 8)
            MUTATED_GENE1 = MUTATED_GENE + 1

            if str(LETHALITY)[-1] == str(MUTATED_GENE1):
                CURE = CURE - RESEARCH
                CURE = abs(CURE)

            elif str(LETHALITY)[-1] == str(MUTATED_GENE):
                INFECTIVITY = INFECTIVITY - RESEARCH
                INFECTIVITY = abs(INFECTIVITY)

        BATCH_INFECTED = random.randint(1, 100)
        BATCH_BORN = random.randint(1, 100)

        _POPULATION_INFECTED = math.exp(INFECTIVITY)
        _POPULATION_INFECTED = BATCH_INFECTED * _POPULATION_INFECTED
        _POPULATION_INFECTED = math.ceil(_POPULATION_INFECTED)
        POPULATION_INFECTED = min(POPULATION_HEALTHY, _POPULATION_INFECTED)

        POPULATION_DEAD = POPULATION_INFECTED * LETHALITY
        POPULATION_DEAD = math.ceil(POPULATION_DEAD)

        TOTAL_INFECTED = TOTAL_INFECTED + POPULATION_INFECTED
        TOTAL_DEAD = TOTAL_DEAD + POPULATION_DEAD

        _BATCH_BORN = math.exp(BIRTH_RATE)
        _BATCH_BORN = math.ceil(_BATCH_BORN)
        BATCH_BORN = BATCH_BORN * _BATCH_BORN

        POPULATION_HEALTHY = POPULATION_HEALTHY - POPULATION_DEAD
        POPULATION_HEALTHY = POPULATION_HEALTHY - POPULATION_INFECTED
        POPULATION_HEALTHY = POPULATION_HEALTHY + BATCH_BORN

        if POPULATION_HEALTHY < 1:
            POPULATION_HEALTHY = POPULATION_HEALTHY + POPULATION_DEAD
            POPULATION_HEALTHY = POPULATION_HEALTHY + POPULATION_INFECTED
            print("\033[91mHUMANITY ERADICATED\033[00m")
            break

    print(f"TIME: {TIME}, CURE: {CURE}, INFECTED: {POPULATION_INFECTED}, DEAD: {POPULATION_DEAD}, HEALTHY: {POPULATION_HEALTHY}")
    TIME += 1

print(f"SEED: {SEED}")
print(
    f"INFECTIVITY: {INFECTIVITY}, LETHALITY: {LETHALITY}, SEVERITY: {SEVERITY}, THRESHOLD: {CURE_THRESHOLD}")
print(f"INFECTED: {TOTAL_INFECTED} ({round(TOTAL_INFECTED / POPULATION_TOTAL * 100, 2)}%)")
print(f"DEAD: {TOTAL_DEAD} ({round(TOTAL_DEAD / POPULATION_TOTAL * 100, 2)}%)")
print(
    f"INFECTED BUT ALIVE: {TOTAL_INFECTED - TOTAL_DEAD} ({round((TOTAL_INFECTED - TOTAL_DEAD) / POPULATION_TOTAL * 100, 2)}%)")
print(f"ALIVE: {POPULATION_HEALTHY + (TOTAL_INFECTED - TOTAL_DEAD)} ({round((POPULATION_HEALTHY + (TOTAL_INFECTED - TOTAL_DEAD)) / POPULATION_TOTAL * 100, 2)}%)")
print(f"HEALTHY: {POPULATION_HEALTHY} ({round(POPULATION_HEALTHY / POPULATION_TOTAL * 100, 2)}%)")
