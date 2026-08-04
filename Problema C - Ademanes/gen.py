#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Generador de casos para "Renata y los ademanes"
# Crea archivos en la carpeta cases/ con nombres: subtarea-{subtask}.{case}.in

import os
import random

OUTDIR = "cases"
os.makedirs(OUTDIR, exist_ok=True)
random.seed(123456)  # reproducible

def write_case(subtask, idx, N, M, S, P):
    fname = f"subtarea-{subtask}.{idx}.in"
    path = os.path.join(OUTDIR, fname)
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"{N} {M}\n")
        f.write(S + "\n")
        f.write(P + "\n")
    print("Wrote", path)

def repeat_char(c, n): return c * n
def alt(c1, c2, n): return "".join(c1 if i%2==0 else c2 for i in range(n))
def random_string(n):
    return "".join(random.choice("<>") for _ in range(n))

# Helper to produce a string that contains many overlapping occurrences of P
def build_overlapping_S(P, repeats, extra_tail=""):
    # concatenate P with overlaps by appending P[1:] repeatedly to maximize overlaps
    if len(P) <= 1:
        return P * repeats + extra_tail
    s = P
    for _ in range(repeats-1):
        s += P[1:]
    s += extra_tail
    return s

# ---------- Subtarea 1: 10 casos (N <= 20, M <= 20) ----------
sub = 1
cases = []
# 1: trivial small, P length 1, S contains it many times
cases.append((5,1, "<><><", "<"))
# 2: trivial small, S already safe
cases.append((3,1, ">>>", "<"))
# 3: M > N
cases.append((5,6, "<><><", "<><><>"))
# 4: S == P
cases.append((6,6, "<><><>", "<><><>"))
# 5: all same char, P same char
cases.append((10,3, ">>>>>>>>>>", ">>>"))
# 6: alternating pattern, P alternating
cases.append((12,3, alt("<", ">", 12), "<><"))
# 7: small exhaustive-ish
cases.append((8,4, "<><<<><>", "><><"))
# 8: M = N = 1
cases.append((1,1, "<", "<"))
# 9: M = 2, overlapping P like "><>"
cases.append((7,3, "><><><>", "><>"))
# 10: random small
cases.append((20,5, random_string(20), random_string(5)))

for i,(N,M,S,P) in enumerate(cases, start=1):
    write_case(sub, i, N, M, S, P)

# ---------- Subtarea 2: 15 casos (N <= 1000, M <= 100) ----------
sub = 2
cases2 = []
# 1: N small, M small
cases2.append((20,5, alt("<", ">", 20), "<><><"))
# 2: N medium, P single char
cases2.append((100,1, random_string(100), "<"))
# 3: N medium, P not present
cases2.append((150,3, ">"*150, "<><"))
# 4: repeated P many times
P = "<><"
S = build_overlapping_S(P, 30, extra_tail="<>")
cases2.append((len(S), len(P), S, P))
# 5: random
cases2.append((200,10, random_string(200), random_string(10)))
# 6: P equals alternating of length 50
cases2.append((300,50, alt("<", ">", 300), alt("<", ">", 50)))
# 7: S contains many disjoint occurrences
P = "<<<>>>"
S = ("x" )  # placeholder
S = "<<<>>>"+">"*50+"<<<>>>"+ "<"*30 + "<<<>>>"
cases2.append((len(S), len(P), S, P))
# 8: M > N
cases2.append((50,60, random_string(50), random_string(60)))
# 9: S all '<', P alternating
cases2.append((120,4, "<"*120, "<><>"))
# 10: S all '>', P '>'
cases2.append((80,1, ">"*80, ">"))
# 11: random
cases2.append((500,20, random_string(500), random_string(20)))
# 12: crafted overlapping P like "<<<" (self-overlap)
cases2.append((200,3, build_overlapping_S("<<<", 50), "<<<"))
# 13: P long but <=100
cases2.append((1000,100, random_string(1000), random_string(100)))
# 14: alternating with one flip to break many matches
S = alt("<", ">", 200)
S = S[:100] + "<" + S[101:]
cases2.append((200,3, S, "<><"))
# 15: small edge
cases2.append((1,1, ">", "<"))

for i,(N,M,S,P) in enumerate(cases2, start=1):
    write_case(sub, i, N, M, S, P)

# ---------- Subtarea 3: 10 casos (M <= 20, focus on small M) ----------
sub = 3
cases3 = []
# exhaustive-like: N=20, M=20 (equal)
cases3.append((20,20, random_string(20), random_string(20)))
# M=20 but S shorter
cases3.append((10,20, random_string(10), random_string(20)))
# M small, many overlaps
cases3.append((20,3, build_overlapping_S("<><", 10), "<><"))
# all '<' with P of mixed
cases3.append((20,5, "<"*20, "<><><"))
# alternating S, P single char
cases3.append((20,1, alt("<", ">", 20), ">"))
# random small
cases3.append((15,4, random_string(15), random_string(4)))
# P equals "><><"
cases3.append((18,4, "><><><><><><><><", "><><"))
# M=2, many positions
cases3.append((20,2, random_string(20), "<>"))
# M=19 near limit
cases3.append((20,19, random_string(20), random_string(19)))
# M=1 edge
cases3.append((20,1, "<"*10 + ">"*10, "<"))

for i,(N,M,S,P) in enumerate(cases3, start=1):
    write_case(sub, i, N, M, S, P)

# ---------- Subtarea 4: 25 casos (N up to 2e5, M <= 100) ----------
sub = 4
cases4 = []
# 1: N large, M small, alternating S
cases4.append((200000,3, alt("<", ">", 200000), "<><"))
# 2: N large, P single char
cases4.append((200000,1, ">"*200000, "<"))
# 3: N large, P not present
cases4.append((200000,2, "<"*200000, "><"))
# 4: N large, P repeated overlapping
P = "<><><"
S = build_overlapping_S(P, 40000)  # will be long; but ensure length <= 200000
S = S[:200000]
cases4.append((len(S), len(P), S, P))
# 5: N large, P length 100 (max for subtask)
cases4.append((200000,100, random_string(200000), random_string(100)))
# 6: many small blocks
S = ("<"*50000) + (">"*50000) + ("<"*50000) + (">"*50000)
cases4.append((len(S), 4, S, "<><>"))
# 7: alternating with one long tail
S = alt("<", ">", 199990) + "<"*10
cases4.append((len(S), 5, S, "<><><"))
# 8: P self-overlapping pattern
P = "<<<>>>"
S = build_overlapping_S(P, 30000)[:200000]
cases4.append((len(S), len(P), S, P))
# 9: random large
cases4.append((150000,50, random_string(150000), random_string(50)))
# 10: M > N (small N)
cases4.append((50,60, random_string(50), random_string(60)))
# 11..25: mix of random and crafted
for k in range(11,26):
    if k % 3 == 0:
        N = 200000
        M = 100
        S = random_string(N)
        P = random_string(M)
    elif k % 3 == 1:
        N = 200000
        M = 10
        # make S with many occurrences of a short P
        P = "<><><><><"
        S = build_overlapping_S(P, 40000)[:N]
    else:
        N = 100000
        M = 20
        S = alt("<", ">", N)
        P = alt("<", ">", M)
    cases4.append((N,M,S,P))

for i,(N,M,S,P) in enumerate(cases4, start=1):
    write_case(sub, i, N, M, S, P)

# ---------- Subtarea 5: 15 casos (full constraints: N up to 2e5, M up to 400) ----------
sub = 5
cases5 = []
# 1: N max, M max
cases5.append((200000,400, random_string(200000), random_string(400)))
# 2: N max, P single char
cases5.append((200000,1, "<"*200000, ">"))
# 3: N max, P length 400 but repetitive to cause overlaps
P = ("<>" * 200)  # length 400
S = build_overlapping_S(P, 1000)[:200000]
cases5.append((len(S), len(P), S, P))
# 4: N max, P not present
cases5.append((200000,50, ">"*200000, "<"*50))
# 5: N small, M large (M>N)
cases5.append((100,200, random_string(100), random_string(200)))
# 6: alternating S, P long alternating
cases5.append((200000,300, alt("<", ">", 200000), alt("<", ">", 300)))
# 7: S equals P repeated many times
P = random_string(100)
S = P * (200000 // len(P))
S = S[:200000]
cases5.append((len(S), len(P), S, P))
# 8: many disjoint occurrences
P = "<"*20
S = (P + ">"*50) * 2000
S = S[:200000]
cases5.append((len(S), len(P), S, P))
# 9: self-overlap worst-case
P = "<" * 400  # all same char, maximum M
S = "<" * 200000
cases5.append((200000,400,S,P))
# 10..15: random large cases
for k in range(10,16):
    N = random.choice([50000,100000,150000,200000])
    M = random.randint(1,400)
    S = random_string(N)
    P = random_string(M)
    cases5.append((N,M,S,P))

for i,(N,M,S,P) in enumerate(cases5, start=1):
    write_case(sub, i, N, M, S, P)

print("Generación completada. Archivos en:", OUTDIR)
