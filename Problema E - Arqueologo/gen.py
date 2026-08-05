#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de casos para el problema "Arqueólogo".
Crea archivos en la carpeta 'cases/' con nombres:
  subtarea-{subtask}.{case}.in
"""

import os
import random
from math import ceil, log2

random.seed(123456)  # semilla fija para reproducibilidad

OUTDIR = "cases"
os.makedirs(OUTDIR, exist_ok=True)

def write_case(subtask, idx, n, L, values, edges):
    fname = os.path.join(OUTDIR, f"subtarea-{subtask}.{idx}.in")
    with open(fname, "w", encoding="utf-8") as f:
        f.write(f"{n} {L}\n")
        f.write(" ".join(str(x) for x in values) + "\n")
        for u, v in edges:
            f.write(f"{u} {v}\n")

# Generadores de árboles
def path_tree(n):
    edges = [(i, i+1) for i in range(1, n)]
    return edges

def star_tree(n):
    edges = [(1, i) for i in range(2, n+1)]
    return edges

def random_tree(n):
    # Pruebas: conectar cada nodo i>1 con un padre aleatorio en [1, i-1]
    edges = []
    for i in range(2, n+1):
        p = random.randint(1, i-1)
        edges.append((p, i))
    return edges

def balanced_binary_tree(n):
    # Construye un árbol parecido a un árbol binario por índices
    edges = []
    for i in range(2, n+1):
        p = i // 2
        edges.append((p, i))
    return edges

def comb_tree(n):
    # "Peine": camino principal con hojas colgando
    edges = []
    for i in range(1, n//2 + 1):
        if 2*i <= n:
            edges.append((i, 2*i))
        if 2*i+1 <= n:
            edges.append((i, 2*i+1))
    # Si faltan nodos, conéctalos aleatoriamente
    used = set()
    for u,v in edges:
        used.add(u); used.add(v)
    cur = max(used) if used else 1
    for i in range(cur+1, n+1):
        p = random.randint(1, n-1)
        edges.append((p, i))
    # Si hay menos de n-1 aristas, completar con path
    while len(edges) < n-1:
        a = random.randint(1, n-1)
        b = random.randint(a+1, n)
        if (a,b) not in edges and (b,a) not in edges:
            edges.append((a,b))
    return edges[:n-1]

# Valores
def values_all_zero(n):
    return [0]*n

def values_random_small(n, maxv=100):
    return [random.randint(0, maxv) for _ in range(n)]

def values_random_large(n, maxv=10**9):
    return [random.randint(0, maxv) for _ in range(n)]

def values_increasing(n, start=1):
    return [start + i for i in range(n)]

def values_heavy_one(n, heavy_idx=1, heavy_val=10**9):
    vals = [random.randint(0, 100) for _ in range(n)]
    vals[heavy_idx-1] = heavy_val
    return vals

# Helpers para crear casos variados
def clamp_L(L):
    return max(1, min(1000, L))

case_counters = {1:0, 2:0, 3:0, 4:0, 5:0}

def add_case(subtask, n, L, values, edges):
    case_counters[subtask] += 1
    write_case(subtask, case_counters[subtask], n, L, values, edges)

# -------------------------
# Subtarea 1: N <= 20, L <= 20 (5 casos)
# -------------------------
# 1) mínimo: N=1
add_case(1, 1, 1, [5], [])  # trivial

# 2) pequeño árbol aleatorio
n = 7; L = 5
add_case(1, n, L, values_random_small(n, 20), random_tree(n))

# 3) camino corto
n = 10; L = 9
add_case(1, n, L, values_increasing(n, 1), path_tree(n))

# 4) estrella con ceros
n = 12; L = 6
add_case(1, n, L, values_all_zero(n), star_tree(n))

# 5) caso límite N=20, L=20, valores grandes
n = 20; L = 20
add_case(1, n, L, values_random_large(n, 10**6), random_tree(n))

# -------------------------
# Subtarea 2: El árbol es un camino (15 casos)
# -------------------------
# Generar caminos de tamaños variados
path_sizes = [2, 3, 5, 10, 20, 50, 100, 150, 200, 300, 400, 600, 800, 1000]
# Queremos 15 casos; si la lista es menor, repetir con variaciones
i = 0
while case_counters[2] < 15:
    if i < len(path_sizes):
        n = path_sizes[i]
    else:
        n = random.choice([5, 30, 75, 250, 500, 1000])
    # L variaciones: very small, medium, max
    if case_counters[2] % 3 == 0:
        L = max(1, n//4)
    elif case_counters[2] % 3 == 1:
        L = min(1000, n-1)
    else:
        L = min(1000, n*2)  # allow extra moves
    vals = values_random_large(n, 10**7)
    add_case(2, n, clamp_L(L), vals, path_tree(n))
    i += 1

# -------------------------
# Subtarea 3: Miguel debe regresar a la ciudad 1 (10 casos)
# -------------------------
# Aunque la entrada no cambia, generamos casos que prueban la necesidad de volver.
# Incluimos L pares (permiten volver) y L impares (no alcanzan a volver).
for n,L,gen in [
    (5, 4, random_tree),
    (5, 3, random_tree),
    (10, 8, balanced_binary_tree),
    (10, 7, balanced_binary_tree),
    (20, 18, comb_tree),
    (20, 19, comb_tree),
    (50, 40, random_tree),
    (50, 41, random_tree),
    (100, 90, balanced_binary_tree),
    (100, 91, balanced_binary_tree),
]:
    vals = values_random_small(n, 200)
    add_case(3, n, clamp_L(L), vals, gen(n))

# -------------------------
# Subtarea 4: N <= 300, L <= 300 (10 casos)
# -------------------------
# Casos variados hasta 300
sizes = [2, 3, 10, 50, 100, 150, 200, 250, 300, 300]
for idx, n in enumerate(sizes, start=1):
    if idx % 4 == 0:
        edges = star_tree(n)
    elif idx % 4 == 1:
        edges = random_tree(n)
    elif idx % 4 == 2:
        edges = path_tree(n)
    else:
        edges = balanced_binary_tree(n)
    # L around limits
    if idx % 3 == 0:
        L = min(300, n-1)
    elif idx % 3 == 1:
        L = min(300, n//2)
    else:
        L = min(300, n*2)
    # values: mix zeros and large
    if idx % 2 == 0:
        vals = values_random_large(n, 10**9)
    else:
        vals = values_random_small(n, 500)
    add_case(4, n, clamp_L(L), vals, edges)

# -------------------------
# Subtarea 5: Sin restricciones (35 casos)
# -------------------------
# Incluir muchos casos grandes, extremos y aleatorios
# 1) varios casos pequeños/medianos
for n in [1,2,3,5,7,9,13,17,23,31]:
    L = random.randint(1, min(1000, max(1, n*2)))
    vals = values_random_large(n, 10**9)
    add_case(5, n, L, vals, random_tree(n))

# 2) muchos casos grandes con N hasta 1000
big_sizes = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
for n in big_sizes:
    # generar 2 casos por tamaño con distinta estructura
    L1 = random.randint(1, 1000)
    L2 = random.randint(max(1, n-1), 1000)
    vals1 = values_random_large(n, 10**9)
    vals2 = values_heavy_one(n, heavy_idx=random.randint(1,n), heavy_val=10**9)
    add_case(5, n, L1, vals1, random_tree(n))
    if case_counters[5] >= 35:
        break
    add_case(5, n, L2, vals2, star_tree(n))
    if case_counters[5] >= 35:
        break

# 3) completar hasta 35 con casos mixtos (camino, balanced, comb)
while case_counters[5] < 35:
    n = random.choice([20, 30, 40, 60, 120, 250, 333, 444, 555])
    typ = random.choice(["path","balanced","comb","random"])
    if typ == "path":
        edges = path_tree(n)
    elif typ == "balanced":
        edges = balanced_binary_tree(n)
    elif typ == "comb":
        edges = comb_tree(n)
    else:
        edges = random_tree(n)
    L = random.randint(1, 1000)
    # sometimes many zeros, sometimes large
    if random.random() < 0.2:
        vals = values_all_zero(n)
    elif random.random() < 0.5:
        vals = values_random_small(n, 1000)
    else:
        vals = values_random_large(n, 10**9)
    add_case(5, n, L, vals, edges)

# Summary print
print("Generación completada. Resumen de archivos creados por subtarea:")
for s in sorted(case_counters.keys()):
    print(f"  Subtarea {s}: {case_counters[s]} casos")
print(f"Archivos escritos en: {OUTDIR}/")
