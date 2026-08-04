#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# solver_fixed_full.py
# Lee todos los archivos cases/subtarea-*.in y genera cases/subtarea-*.out
# KMP automaton + DP rolling array. Lectura robusta de S y P.

import os
import glob

INF = 10**9

def build_kmp_automaton(P):
    """Construye la tabla de prefijos pi y el autómata nxt[state][ch_idx].
       ch_idx: 0 -> '<', 1 -> '>' """
    m = len(P)
    # prefijo pi
    pi = [0] * m
    for i in range(1, m):
        j = pi[i-1]
        while j > 0 and P[i] != P[j]:
            j = pi[j-1]
        if P[i] == P[j]:
            j += 1
        pi[i] = j

    # autómata para estados 0..m (incluye estado m por completitud)
    nxt = [[0,0] for _ in range(m+1)]
    # orden creciente de estados garantiza que nxt[pi[state-1]] ya esté calculado
    for state in range(0, m+1):
        for ch_idx, ch in enumerate(['<', '>']):
            if state < m and ch == P[state]:
                nxt[state][ch_idx] = state + 1
            else:
                if state == 0:
                    nxt[state][ch_idx] = 0
                else:
                    # usar la transición del prefijo propio
                    nxt[state][ch_idx] = nxt[pi[state-1]][ch_idx]
    return nxt

def solve_instance(N, M, S, P):
    # caso trivial
    if M > N:
        return 0
    if M == 0:
        return 0

    nxt = build_kmp_automaton(P)
    # dp para estados 0..M-1
    dp = [INF] * M
    dp[0] = 0

    for i in range(N):
        ndp = [INF] * M
        orig = S[i]
        for state in range(M):
            cur = dp[state]
            if cur >= INF:
                continue
            # poner '<'
            cost = 0 if orig == '<' else 1
            ns = nxt[state][0]
            if ns != M:
                if cur + cost < ndp[ns]:
                    ndp[ns] = cur + cost
            # poner '>'
            cost = 0 if orig == '>' else 1
            ns = nxt[state][1]
            if ns != M:
                if cur + cost < ndp[ns]:
                    ndp[ns] = cur + cost
        dp = ndp

    ans = min(dp)
    if ans >= INF:
        ans = N
    return ans

def read_exact_string(f, needed):
    """Lee del archivo f y devuelve exactamente needed caracteres válidos '<' o '>'.
       Si EOF antes de alcanzar needed, devuelve lo que haya leído."""
    s = ""
    while len(s) < needed:
        line = f.readline()
        if not line:
            break
        # conservar solo '<' y '>'
        for ch in line:
            if ch == '<' or ch == '>':
                s += ch
                if len(s) >= needed:
                    break
    return s

def process_all_cases(indir="cases"):
    pattern = os.path.join(indir, "subtarea-*.in")
    files = sorted(glob.glob(pattern))
    if not files:
        print("No se encontraron archivos con patrón:", pattern)
        return

    for path in files:
        with open(path, "r", encoding="utf-8") as f:
            header = f.readline()
            if not header:
                print("Formato inválido en", path)
                continue
            parts = header.strip().split()
            if len(parts) < 2:
                print("Formato inválido en header de", path)
                continue
            try:
                N = int(parts[0]); M = int(parts[1])
            except:
                print("Header no numérico en", path)
                continue

            S = read_exact_string(f, N)
            P = read_exact_string(f, M)
            S = S[:N]
            P = P[:M]

            # seguridad adicional: si S es más corto que N, rellenar con '>' arbitrario
            # esto evita crash y representa un caso donde la entrada estaba malformada
            if len(S) < N:
                S = S + '>' * (N - len(S))
            if len(P) < M:
                P = P + '>' * (M - len(P))

        result = solve_instance(N, M, S, P)

        outpath = os.path.splitext(path)[0] + ".out"
        with open(outpath, "w", encoding="utf-8") as fo:
            fo.write(str(result) + "\n")
        print(f"Wrote {outpath}: {result}")

if __name__ == "__main__":
    process_all_cases("cases")
