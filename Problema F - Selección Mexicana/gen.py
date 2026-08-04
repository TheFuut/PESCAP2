#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador corregido de casos para "Selección Mexicana".
Crea archivos en la carpeta cases/ con nombres exactos:
  subtarea-{subtask}.{case}.in

Casos por subtarea:
 - 1: 10 casos (N <= 20)
 - 2: 10 casos (solo tipo 2)
 - 3: 20 casos (N, M <= 5000)
 - 4: 50 casos (límites completos)

Correcciones importantes:
 - Evita rangos vacíos en random.randint.
 - Limita M al número máximo de pares únicos posibles.
 - Garantiza A != B y formato correcto.
"""
import os
import random
from itertools import combinations

random.seed(123456)

OUTDIR = "cases"
os.makedirs(OUTDIR, exist_ok=True)

MAX_N = 2 * 10**5
MAX_M = 4 * 10**5

def write_case(subtask, idx, N, clauses):
    fname = f"subtarea-{subtask}.{idx}.in"
    path = os.path.join(OUTDIR, fname)
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"{N} {len(clauses)}\n")
        for t,a,b in clauses:
            f.write(f"{t} {a} {b}\n")

def clause_satisfied_by_assignment(t, a, b, assign):
    if t == 1:
        return (not assign[a]) or assign[b]
    if t == 2:
        return (not assign[a]) or (not assign[b])
    if t == 3:
        return assign[a] or assign[b]
    return False

def random_clause_satisfied(N, assign, allowed_types=(1,2,3)):
    tries = 0
    while True:
        tries += 1
        if tries > 1000:
            # fallback: pick any valid pair and a type that is satisfied
            a = random.randint(1, N)
            b = random.randint(1, N)
            while b == a:
                b = random.randint(1, N)
            for t in allowed_types:
                if clause_satisfied_by_assignment(t, a, b, assign):
                    return (t, a, b)
            return (2, a, b)
        a = random.randint(1, N)
        b = random.randint(1, N)
        if a == b:
            continue
        t = random.choice(allowed_types)
        if clause_satisfied_by_assignment(t, a, b, assign):
            return (t, a, b)

def make_satisfiable_case(N, M, allowed_types=(1,2,3)):
    assign = {i: random.choice([False, True]) for i in range(1, N+1)}
    clauses = []
    max_pairs = N*(N-1)//2
    use_unique_pairs = (M > max_pairs // 2)  # heuristic to avoid duplicates when many clauses
    seen = set()
    for _ in range(M):
        if use_unique_pairs:
            # generate unique pairs until exhausted
            tries = 0
            while True:
                tries += 1
                if tries > 1000:
                    # fallback to any clause satisfied
                    clauses.append(random_clause_satisfied(N, assign, allowed_types))
                    break
                a = random.randint(1, N)
                b = random.randint(1, N)
                if a == b: continue
                key = (min(a,b), max(a,b))
                if key in seen: continue
                t = random.choice(allowed_types)
                if clause_satisfied_by_assignment(t, a, b, assign):
                    seen.add(key)
                    clauses.append((t,a,b))
                    break
        else:
            clauses.append(random_clause_satisfied(N, assign, allowed_types))
    return clauses, assign

def make_unsat_core(N):
    a = random.randint(1, N)
    b = random.randint(1, N)
    while b == a:
        b = random.randint(1, N)
    return [(1,a,b),(1,b,a),(3,a,b),(2,a,b)]

def make_unsatisfiable_case(N, M, allowed_types=(1,2,3)):
    clauses = []
    core = make_unsat_core(N)
    core = [c for c in core if c[0] in allowed_types]
    if not core:
        a = random.randint(1, N)
        b = random.randint(1, N)
        while b == a:
            b = random.randint(1, N)
        if 1 in allowed_types and 2 in allowed_types:
            core = [(1,a,b),(1,b,a),(2,a,b)]
        elif 2 in allowed_types and 3 in allowed_types:
            core = [(3,a,b),(2,a,b)]
        else:
            core = [(2,a,b),(2,b,a)]
    clauses.extend(core)
    remaining = max(0, M - len(clauses))
    assign = {i: random.choice([False, True]) for i in range(1, N+1)}
    max_pairs = N*(N-1)//2
    seen = set((min(x[1],x[2]), max(x[1],x[2])) for x in clauses)
    for _ in range(remaining):
        # try to add unique pairs if possible
        tries = 0
        while True:
            tries += 1
            if tries > 500:
                clauses.append(random_clause_satisfied(N, assign, allowed_types))
                break
            a = random.randint(1, N)
            b = random.randint(1, N)
            if a == b: continue
            key = (min(a,b), max(a,b))
            if key in seen and len(seen) < max_pairs:
                continue
            t = random.choice(allowed_types)
            if clause_satisfied_by_assignment(t, a, b, assign):
                seen.add(key)
                clauses.append((t,a,b))
                break
    random.shuffle(clauses)
    return clauses

# Utility to safely choose M with bounds and avoid empty ranges
def choose_M(lower, upper):
    if upper < 1:
        return 1
    if lower <= upper:
        return random.randint(lower, upper)
    # if requested lower > upper, fallback to a safe range
    return random.randint(1, upper)

# --- SUBTAREA 1: N <= 20, 10 casos
sub1_cases = []
# 1
sub1_cases.append((2, [(1,1,2)]))
# 2 unsat core
sub1_cases.append((2, [(1,1,2),(1,2,1),(3,1,2),(2,1,2)]))
# 3 random satisfiable
N=5; M=8
clauses,assign = make_satisfiable_case(N,M)
sub1_cases.append((N, clauses))
# 4 unsat
N=7; M=12
clauses = make_unsatisfiable_case(N,M)
sub1_cases.append((N, clauses))
# 5 N=20
N=20; M=40
clauses,assign = make_satisfiable_case(N,M)
sub1_cases.append((N, clauses))
# 6 many type 2
N=10; M=15
clauses = []
for a,b in combinations(range(1, N+1), 2):
    if len(clauses) >= M: break
    clauses.append((2,a,b))
sub1_cases.append((N, clauses))
# 7 repeated constraints
sub1_cases.append((3, [(3,1,2),(3,2,3),(1,1,3),(2,1,2)]))
# 8 random unsat
N=4; M=10
clauses = make_unsatisfiable_case(N,M)
sub1_cases.append((N, clauses))
# 9 chain implications
N=6; M=5
clauses = [(1,i,i+1) for i in range(1,6)]
sub1_cases.append((N, clauses))
# 10 mixed random
N=8; M=20
clauses,assign = make_satisfiable_case(N,M)
sub1_cases.append((N, clauses))

for i,(N,clauses) in enumerate(sub1_cases, start=1):
    # ensure N <= 20
    if N > 20:
        raise ValueError("Subtarea 1: N must be <= 20")
    write_case(1, i, N, clauses)

# --- SUBTAREA 2: solo restricciones tipo 2, 10 casos
sub2_cases = []
# helper to cap M to possible pairs
def unique_pairs_clauses(N, M, t=2):
    max_pairs = N*(N-1)//2
    M = min(M, max_pairs)
    clauses = []
    seen = set()
    while len(clauses) < M:
        a = random.randint(1, N); b = random.randint(1, N)
        if a == b: continue
        key = (min(a,b), max(a,b))
        if key in seen: continue
        seen.add(key)
        clauses.append((t,a,b))
    return clauses

sub2_cases.append((5, [(2,1,2),(2,2,3),(2,3,4),(2,4,5)]))
sub2_cases.append((6, unique_pairs_clauses(6, 15)))
sub2_cases.append((50, unique_pairs_clauses(50, 100)))
sub2_cases.append((100, unique_pairs_clauses(100, 400)))
sub2_cases.append((2, [(2,1,2)]))
sub2_cases.append((20, unique_pairs_clauses(20, 190)))  # complete graph M=190
sub2_cases.append((30, unique_pairs_clauses(30, 60)))
sub2_cases.append((200, unique_pairs_clauses(200, 50)))
sub2_cases.append((500, unique_pairs_clauses(500, 1000)))
sub2_cases.append((1000, unique_pairs_clauses(1000, 1500)))

for i,(N,clauses) in enumerate(sub2_cases, start=1):
    write_case(2, i, N, clauses)

# --- SUBTAREA 3: N,M <= 5000, 20 casos
sub3_cases = []
# helper to cap N and M
def cap_N_M(N, M):
    N = min(N, 5000)
    M = min(M, 5000)
    return N, M

# 1
N, M = cap_N_M(50, 80)
clauses,assign = make_satisfiable_case(N,M)
sub3_cases.append((N,clauses))
# 2 unsat
N, M = cap_N_M(50, 100)
clauses = make_unsatisfiable_case(N,M)
sub3_cases.append((N,clauses))
# 3 chain implications
N = min(500, 5000)
clauses = [(1,i,i+1) for i in range(1, N)]
sub3_cases.append((N, clauses))
# 4 many type 3
N, M = cap_N_M(400, 1000)
clauses,assign = make_satisfiable_case(N,M)
sub3_cases.append((N,clauses))
# 5 many type 2
N, M = cap_N_M(400, 1200)
M = min(M, 5000)
clauses = unique_pairs_clauses(N, M, t=2)
sub3_cases.append((N,clauses))
# 6 mixed random
N, M = cap_N_M(1000, 2000)
clauses,assign = make_satisfiable_case(N,M)
sub3_cases.append((N,clauses))
# 7 unsat + many
N, M = cap_N_M(1000, 3000)
clauses = make_unsatisfiable_case(N,M)
sub3_cases.append((N,clauses))
# 8 trivial unsat
sub3_cases.append((2, [(3,1,2),(2,1,2)]))
# 9 small mix
sub3_cases.append((3, [(1,1,2),(1,2,3),(2,1,3),(3,1,3)]))
# 10 medium random
N, M = cap_N_M(800, 1500)
clauses,assign = make_satisfiable_case(N,M)
sub3_cases.append((N,clauses))

# 11-20 variety
for k in range(11,21):
    if k % 3 == 0:
        N = random.randint(2, 2000)
        M = random.randint(1, min(5000, N*4))
        N, M = cap_N_M(N, M)
        clauses,assign = make_satisfiable_case(N,M)
    elif k % 3 == 1:
        N = random.randint(2, 2000)
        M = random.randint(1, min(5000, N*4))
        N, M = cap_N_M(N, M)
        clauses = make_unsatisfiable_case(N,M)
    else:
        N = random.randint(2, 2000)
        M = random.randint(1, min(5000, N*3))
        N, M = cap_N_M(N, M)
        clauses=[]
        for _ in range(M):
            a=random.randint(1,N); b=random.randint(1,N)
            while b==a: b=random.randint(1,N)
            clauses.append((3,a,b))
    sub3_cases.append((N,clauses))

for i,(N,clauses) in enumerate(sub3_cases, start=1):
    # ensure N,M <= 5000
    if N > 5000 or len(clauses) > 5000:
        raise ValueError("Subtarea 3: N and M must be <= 5000")
    write_case(3, i, N, clauses)

# --- SUBTAREA 4: límites completos, 50 casos
sub4_cases = []

# small ones
sub4_cases.append((2, [(1,1,2)]))
sub4_cases.append((3, [(1,1,2),(1,2,1),(3,1,2),(2,1,2)]))

# large N small M
N=200000; M=10
clauses,assign = make_satisfiable_case(N,M)
sub4_cases.append((N,clauses))

# large N many random clauses (cap M to 400000 and to possible pairs)
N=200000; upper = min(400000, N*(N-1)//2)
M = choose_M(200000, upper)
M = min(M, MAX_M)
# generate M clauses with unique pairs until exhausted
clauses=[]
seen=set()
max_pairs = N*(N-1)//2
M = min(M, max_pairs)
while len(clauses) < M:
    a = random.randint(1,N); b = random.randint(1,N)
    if a==b: continue
    key=(min(a,b),max(a,b))
    if key in seen: continue
    seen.add(key)
    t=random.choice([1,2,3])
    clauses.append((t,a,b))
sub4_cases.append((N,clauses))

# other large cases with safe M selection
N=100000; upper = min(400000, N*(N-1)//2)
M = choose_M(1, upper)
M = min(M, MAX_M)
clauses=[]
seen=set()
M = min(M, N*(N-1)//2)
while len(clauses) < M:
    a = random.randint(1,N); b = random.randint(1,N)
    if a==b: continue
    key=(min(a,b),max(a,b))
    if key in seen: continue
    seen.add(key)
    t=random.choice([1,2,3])
    clauses.append((t,a,b))
sub4_cases.append((N,clauses))

# more large cases (examples)
sub4_cases.append((50000, make_satisfiable_case(50000, 1000)[0]))
sub4_cases.append((100000, unique_pairs_clauses(100000, 150000, t=2)))
sub4_cases.append((200000, make_unsatisfiable_case(200000, 1000)))
sub4_cases.append((100000, [(1,i,i+1) for i in range(1, min(200000,100000))][:200000]))
sub4_cases.append((150000, []))  # placeholder; will fill below

# fill the placeholder with safe random clauses
N = 150000
upper = min(400000, N*(N-1)//2)
M = choose_M(1, upper)
clauses=[]
seen=set()
M = min(M, 400000)
while len(clauses) < M:
    a = random.randint(1,N); b = random.randint(1,N)
    if a==b: continue
    key=(min(a,b),max(a,b))
    if key in seen: continue
    seen.add(key)
    t=random.choice([1,2,3])
    clauses.append((t,a,b))
sub4_cases[-1] = (N, clauses)

# generate remaining cases up to 50 with safe bounds
while len(sub4_cases) < 50:
    mode = random.randint(0,4)
    if mode == 0:
        N = random.randint(2, 200000)
        upper = min(400000, N*(N-1)//2)
        # prefer large M sometimes
        if upper >= 200000:
            M = choose_M(200000, upper)
        else:
            M = choose_M(1, upper)
        M = min(M, 400000)
        # cap M to possible pairs
        M = min(M, N*(N-1)//2)
        clauses=[]
        seen=set()
        while len(clauses) < M:
            a = random.randint(1,N); b = random.randint(1,N)
            if a==b: continue
            key=(min(a,b),max(a,b))
            if key in seen: continue
            seen.add(key)
            t=random.choice([1,2,3])
            clauses.append((t,a,b))
    elif mode == 1:
        N = random.randint(2, 200000)
        M = random.randint(1, min(400000, max(1, N*2)))
        M = min(M, 400000)
        clauses,assign = make_satisfiable_case(N,M)
    elif mode == 2:
        N = random.randint(2, 200000)
        M = random.randint(1, min(400000, max(4, N*2)))
        M = min(M, 400000)
        clauses = make_unsatisfiable_case(N,M)
    elif mode == 3:
        N = random.randint(2, 200000)
        upper = min(400000, N*(N-1)//2)
        M = choose_M(1, upper)
        M = min(M, 400000)
        clauses = unique_pairs_clauses(N, M, t=2)
    else:
        N = random.randint(2, 200000)
        M = random.randint(1, min(400000, N*3))
        M = min(M, 400000)
        clauses=[]
        for _ in range(M):
            a=random.randint(1,N); b=random.randint(1,N)
            while b==a: b=random.randint(1,N)
            clauses.append((3,a,b))
    sub4_cases.append((N,clauses))

# write first 50 cases
for i,(N,clauses) in enumerate(sub4_cases[:50], start=1):
    # final safety checks
    if not (2 <= N <= 200000):
        raise ValueError("Subtarea 4: N fuera de rango")
    if not (1 <= len(clauses) <= 400000):
        raise ValueError("Subtarea 4: M fuera de rango")
    write_case(4, i, N, clauses)

print("Generación completada. Archivos escritos en la carpeta 'cases/'.")
