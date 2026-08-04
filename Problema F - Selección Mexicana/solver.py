#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
solver.py
Lee todos los archivos .in en la carpeta 'cases/' y genera .out con "SI"/"NO".
Implementación 2-SAT mediante grafo de implicaciones y Kosaraju iterativo.
"""
import os
import sys
from collections import deque

CASES_DIR = "cases"

def var_index_true(i):
    # i: 1-based variable index
    return 2 * (i - 1)

def var_index_false(i):
    return var_index_true(i) ^ 1  # true^1 = false

def add_implication(g, gr, u, v):
    g[u].append(v)
    gr[v].append(u)

def solve_instance(N, clauses):
    # Build graph with 2*N nodes: for var i (1..N): true = 2*(i-1), false = true^1
    nodes = 2 * N
    g = [[] for _ in range(nodes)]
    gr = [[] for _ in range(nodes)]

    for t, a, b in clauses:
        if t == 1:
            # If A then B  => (!A or B)
            # A_true -> B_true
            # B_false -> A_false
            add_implication(g, gr, var_index_true(a), var_index_true(b))
            add_implication(g, gr, var_index_false(b), var_index_false(a))
        elif t == 2:
            # Not both => (!A or !B)
            # A_true -> B_false
            # B_true -> A_false
            add_implication(g, gr, var_index_true(a), var_index_false(b))
            add_implication(g, gr, var_index_true(b), var_index_false(a))
        elif t == 3:
            # At least one => (A or B) => (!A -> B) and (!B -> A)
            add_implication(g, gr, var_index_false(a), var_index_true(b))
            add_implication(g, gr, var_index_false(b), var_index_true(a))
        else:
            # Should not happen
            pass

    # Kosaraju iterative
    visited = [False] * nodes
    order = []

    # First pass: compute finish order (iterative DFS)
    for s in range(nodes):
        if visited[s]:
            continue
        stack = [(s, 0)]  # (node, next_child_index)
        while stack:
            v, idx = stack[-1]
            if not visited[v]:
                visited[v] = True
            # find next unvisited neighbor
            g_v = g[v]
            while idx < len(g_v) and visited[g_v[idx]]:
                idx += 1
            if idx < len(g_v):
                # update current frame's next index
                stack[-1] = (v, idx + 1)
                to = g_v[idx]
                if not visited[to]:
                    stack.append((to, 0))
            else:
                # finished v
                order.append(v)
                stack.pop()

    # Second pass: assign components on reversed graph
    comp = [-1] * nodes
    cid = 0
    for v in reversed(order):
        if comp[v] != -1:
            continue
        # iterative DFS on gr to mark component cid
        stack = [v]
        comp[v] = cid
        while stack:
            u = stack.pop()
            for w in gr[u]:
                if comp[w] == -1:
                    comp[w] = cid
                    stack.append(w)
        cid += 1

    # Check for contradictions: var and its negation in same component
    for i in range(1, N+1):
        t_idx = var_index_true(i)
        f_idx = var_index_false(i)
        if comp[t_idx] == comp[f_idx]:
            return False
    return True

def process_file(path_in, path_out):
    with open(path_in, "r", encoding="utf-8") as f:
        first = f.readline().strip().split()
        if not first:
            raise ValueError(f"Archivo vacío o mal formado: {path_in}")
        N = int(first[0])
        M = int(first[1])
        clauses = []
        for _ in range(M):
            line = f.readline()
            if not line:
                raise ValueError(f"Archivo {path_in} indica M={M} pero tiene menos líneas.")
            parts = line.strip().split()
            if len(parts) != 3:
                raise ValueError(f"Línea mal formada en {path_in}: {line!r}")
            t = int(parts[0]); a = int(parts[1]); b = int(parts[2])
            if a == b:
                # Although generator avoids A==B, handle gracefully:
                # For safety, skip or treat accordingly. We'll keep as-is (invalid) but solver can handle.
                pass
            clauses.append((t,a,b))
    sat = solve_instance(N, clauses)
    with open(path_out, "w", encoding="utf-8") as f:
        f.write("SI\n" if sat else "NO\n")

def main():
    if not os.path.isdir(CASES_DIR):
        print(f"Carpeta '{CASES_DIR}' no encontrada.", file=sys.stderr)
        sys.exit(1)

    files = sorted([fn for fn in os.listdir(CASES_DIR) if fn.endswith(".in")])
    if not files:
        print("No se encontraron archivos .in en 'cases/'.", file=sys.stderr)
        sys.exit(1)

    for fn in files:
        path_in = os.path.join(CASES_DIR, fn)
        base = fn[:-3]
        path_out = os.path.join(CASES_DIR, base + ".out")
        try:
            process_file(path_in, path_out)
            print(f"Procesado: {fn} -> {base}.out")
        except Exception as e:
            print(f"Error procesando {fn}: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
