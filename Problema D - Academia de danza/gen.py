#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Generador de casos para "Academia de danza"
# Crea archivos en cases/subtarea-{subtask}.{case}.in

import os
import random

OUTDIR = "cases"
os.makedirs(OUTDIR, exist_ok=True)

MAX_A = 10**9
MAX_B = 10**9

def write_case(subtask, idx, pairs):
    fname = f"subtarea-{subtask}.{idx}.in"
    path = os.path.join(OUTDIR, fname)
    with open(path, "w", encoding="utf-8") as f:
        f.write(str(len(pairs)) + "\n")
        for a,b in pairs:
            f.write(f"{a} {b}\n")
    print("Wrote", path)

def random_pairs(n, a_range=(1,MAX_A), b_range=(1,MAX_B), seed=None):
    if seed is not None:
        random.seed(seed)
    return [(random.randint(*a_range), random.randint(*b_range)) for _ in range(n)]

# ---------- Subtarea 1: 10 casos, N <= 2000 ----------
# Casos: muy pequeños, duplicados, ordenados, inversos, límite 2000
sub1_cases = []

# 1. N = 1
sub1_cases.append([(1,1)])

# 2. N = 5 small random
sub1_cases.append(random_pairs(5, seed=1))

# 3. All equal pairs
sub1_cases.append([(10,10)] * 10)

# 4. Same a, different b (duplicates in a)
sub1_cases.append([(5, i) for i in [1,2,2,3,5,5,6]])

# 5. Same b, different a
sub1_cases.append([(i, 7) for i in [1,2,3,4,5,6,7]])

# 6. Strictly increasing already
sub1_cases.append([(i, i+1) for i in range(1,21)])

# 7. Strictly decreasing
sub1_cases.append([(i, 100-i) for i in range(20,0,-1)])

# 8. Mixed with ties and random
sub1_cases.append([(2,3),(2,2),(3,4),(4,1),(5,5)])  # example from enunciado

# 9. N = 2000 random (upper for subtask1)
sub1_cases.append(random_pairs(2000, seed=9))

# 10. Many duplicates small values
pairs = []
for _ in range(200):
    pairs.append((1,1))
for i in range(1,51):
    pairs.append((i%5+1, i%7+1))
sub1_cases.append(pairs)

for i,p in enumerate(sub1_cases, start=1):
    write_case(1, i, p)

# ---------- Subtarea 2: 10 casos, N <= 10000 ----------
# Casos: medianos, adversos para LIS, many duplicates, random
sub2_cases = []

# 1. N = 10 small
sub2_cases.append(random_pairs(10, seed=21))

# 2. N = 100 increasing a, random b
sub2_cases.append([(i, random.randint(1,1000)) for i in range(1,101)])

# 3. N = 100 decreasing b to force small LIS
sub2_cases.append([(i, 100-i) for i in range(1,101)])

# 4. Many with same a but b descending (classic trap)
pairs = []
for a in range(1,51):
    for b in range(50,0,-1):
        pairs.append((a, b))
sub2_cases.append(pairs[:500])  # keep <=10000

# 5. Random N = 1000
sub2_cases.append(random_pairs(1000, seed=25))

# 6. Alternating pattern to create long LIS on b after sorting by a
pairs = []
for i in range(1,501):
    pairs.append((i, i%2 + i//2))
sub2_cases.append(pairs)

# 7. Many duplicates in b
pairs = []
for i in range(1,501):
    pairs.append((random.randint(1,200), 5))
sub2_cases.append(pairs)

# 8. N = 10000 random (upper for subtask2)
sub2_cases.append(random_pairs(10000, seed=28))

# 9. Edge values near 1e9
pairs = []
for i in range(1,501):
    pairs.append((MAX_A - i, MAX_B - (i*2 % 1000)))
sub2_cases.append(pairs)

# 10. Crafted: same a many times, b increasing within same a
pairs = []
for a in range(1,201):
    for j in range(1,6):
        pairs.append((a, j))
sub2_cases.append(pairs)

for i,p in enumerate(sub2_cases, start=1):
    write_case(2, i, p)

# ---------- Subtarea 3: 25 casos, N <= 50000, all a distinct ----------
# Must ensure all a distinct in each case
sub3_cases = []

# Helper to create distinct-a random pairs
def distinct_a_pairs(n, a_start=1, seed=None):
    if seed is not None:
        random.seed(seed)
    a_vals = list(range(a_start, a_start + n))
    random.shuffle(a_vals)
    return [(a_vals[i], random.randint(1, MAX_B)) for i in range(n)]

# 1. N = 1
sub3_cases.append(distinct_a_pairs(1, seed=31))

# 2. N = 10
sub3_cases.append(distinct_a_pairs(10, seed=32))

# 3. N = 100
sub3_cases.append(distinct_a_pairs(100, seed=33))

# 4. N = 1000
sub3_cases.append(distinct_a_pairs(1000, seed=34))

# 5. N = 5000
sub3_cases.append(distinct_a_pairs(5000, seed=35))

# 6. N = 50000 with random b
sub3_cases.append(distinct_a_pairs(50000, seed=36))

# 7. Increasing b with distinct a (best case)
pairs = [(i, i) for i in range(1,2001)]
sub3_cases.append(pairs)

# 8. Decreasing b with distinct a (worst LIS)
pairs = [(i, 2001-i) for i in range(1,2001)]
sub3_cases.append(pairs)

# 9. Zigzag b to create moderate LIS
pairs = []
for i in range(1,5001):
    pairs.append((i, (i%100)* (1 if i%2==0 else -1) + 1000))
# adjust to positive
pairs = [(a, abs(b)%MAX_B + 1) for a,b in pairs]
sub3_cases.append(pairs)

# 10. Many equal b but distinct a
pairs = [(i, 123456) for i in range(1,3001)]
sub3_cases.append(pairs)

# 11-25: mix of sizes and patterns ensuring distinct a
sizes = [50, 200, 800, 1500, 2500, 4000, 7000, 12000, 20000, 30000, 45000, 49999, 25000, 35000, 100]
seeds = list(range(40, 55))
for s,seed in zip(sizes, seeds):
    sub3_cases.append(distinct_a_pairs(s, seed=seed))

# Ensure we have exactly 25 cases
sub3_cases = sub3_cases[:25]

for i,p in enumerate(sub3_cases, start=1):
    # sort by a to avoid accidental duplicate a generation issues in some patterns
    # but keep a distinct property
    write_case(3, i, p)

# ---------- Subtarea 4: 35 casos, N <= 2e5 ----------
# Full constraints, include N = 200000, large values, adversarial patterns
sub4_cases = []

# 1. N = 1
sub4_cases.append([(1,1)])

# 2. Small random
sub4_cases.append(random_pairs(10, seed=61))

# 3. N = 1000 random
sub4_cases.append(random_pairs(1000, seed=62))

# 4. N = 10000 random
sub4_cases.append(random_pairs(10000, seed=63))

# 5. N = 50000 random
sub4_cases.append(random_pairs(50000, seed=64))

# 6. N = 100000 random
sub4_cases.append(random_pairs(100000, seed=65))

# 7. N = 200000 random (max size)
sub4_cases.append(random_pairs(200000, seed=66))

# 8. All pairs equal (large N)
sub4_cases.append([(7,7)] * 100000)

# 9. All a equal, b increasing
pairs = [(42, i) for i in range(1,50001)]
sub4_cases.append(pairs)

# 10. All a equal, b decreasing
pairs = [(42, 50001-i) for i in range(1,50001)]
sub4_cases.append(pairs)

# 11. All b equal, a increasing
pairs = [(i, 999999937) for i in range(1,100001)]
sub4_cases.append(pairs)

# 12. Alternating large/small to break naive solutions
pairs = []
for i in range(1,100001):
    if i%2==0:
        pairs.append((i, MAX_B - i))
    else:
        pairs.append((i, i))
sub4_cases.append(pairs)

# 13. Many duplicates with occasional increasing run
pairs = []
for i in range(1,150001):
    if i%1000==0:
        pairs.append((i, i))
    else:
        pairs.append((i%500+1, i%100+1))
sub4_cases.append(pairs)

# 14. Values near 1e9
pairs = []
for i in range(200000, 200000-50000, -1):
    pairs.append((MAX_A - i, MAX_B - (i*3 % 100000)))
sub4_cases.append(pairs)

# 15. Strictly increasing both a and b
pairs = [(i, i) for i in range(1,50001)]
sub4_cases.append(pairs)

# 16-35: additional mixes to reach 35 cases
more_sizes = [20, 200, 2000, 8000, 16000, 32000, 64000, 120000, 180000, 199999,
              25000, 47000, 53000, 75000, 90000, 110000, 140000, 170000, 190000, 200000]
seed = 80
for s in more_sizes:
    sub4_cases.append(random_pairs(s, seed=seed))
    seed += 1

# Trim or pad to exactly 35
sub4_cases = sub4_cases[:35]

for i,p in enumerate(sub4_cases, start=1):
    write_case(4, i, p)

print("Generation complete. Files are in the 'cases' directory.")
