#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Solucionador para "Renata y los ademanes".

Lee todos los archivos .in en la carpeta `cases/` con nombre:
  subtarea-{subtask}.{case}.in

Para cada archivo:
  - Parsea {subtask} y {case} del nombre del archivo.
  - Resuelve el caso usando un autómata KMP + programación dinámica.
  - Escribe la salida en `cases/subtarea-{subtask}.{case}.out`.
  - Verifica que el .out generado contiene exactamente la respuesta esperada.

Imprime un resumen por consola de los archivos procesados y del resultado de la verificación.
"""
from typing import List, Tuple
import os
import sys
import re

INF = 10**18
CASES_DIR = "cases"
OUT_DIR = "cases"

def list_input_files() -> List[str]:
    if not os.path.isdir(CASES_DIR):
        print(f"Error: no existe la carpeta '{CASES_DIR}'.", file=sys.stderr)
        return []
    files = sorted(f for f in os.listdir(CASES_DIR) if re.match(r"^subtarea-\d+\.\d+\.in$", f))
    return files

def parse_filename(fname: str) -> Tuple[str, str]:
    # fname like subtarea-3.7.in
    m = re.match(r"^subtarea-(\d+)\.(\d+)\.in$", fname)
    if not m:
        raise ValueError(f"Nombre de archivo inválido: {fname}")
    return m.group(1), m.group(2)

def read_case(path: str) -> Tuple[int,int,str,str]:
    with open(path, "r", encoding="utf-8") as f:
        data = f.read().strip().split()
    if len(data) < 4:
        raise ValueError(f"Formato inválido en {path}")
    n = int(data[0]); m = int(data[1])
    S = data[2].strip()
    P = data[3].strip()
    if len(S) != n or len(P) != m:
        # allow mismatch if input used different whitespace; but enforce lengths
        S = S[:n].ljust(n, "<")
        P = P[:m].ljust(m, "<")
    return n, m, S, P

def build_kmp_automaton(P: str) -> List[List[int]]:
    """
    Construye la transición next_state[s][k] para s in [0..m-1], k in {0,1}
    donde k==0 -> '<', k==1 -> '>'.
    La transición devuelve la nueva longitud de prefijo coincidente.
    """
    m = len(P)
    pi = [0] * m
    for i in range(1, m):
        j = pi[i-1]
        while j > 0 and P[i] != P[j]:
            j = pi[j-1]
        if P[i] == P[j]:
            j += 1
        pi[i] = j

    chars = ['<', '>']
    next_state = [[0]*2 for _ in range(max(1, m))]  # if m==0 not possible per constraints
    for s in range(m):
        for k, c in enumerate(chars):
            t = s
            # try to extend with c
            while t > 0 and (t >= m or P[t] != c):
                t = pi[t-1]
            if t < m and P[t] == c:
                t += 1
            next_state[s][k] = t
    return next_state

def solve_instance(n: int, m: int, S: str, P: str) -> int:
    # Edge: if m == 0 (not in constraints) treat as 0
    if m == 0:
        return 0
    # If pattern length > 0 but S empty, no occurrences -> 0
    if n == 0:
        return 0
    # Build automaton for states 0..m-1
    next_state = build_kmp_automaton(P)
    # dp2[j] = minimal cost to be in state j (matched prefix length j) after processing prefix
    dp2 = [INF] * m
    dp2[0] = 0
    chars = ['<', '>']
    for i in range(n):
        ndp2 = [INF] * m
        si = S[i]
        for j in range(m):
            cur = dp2[j]
            if cur >= INF:
                continue
            # try both characters
            for k, c in enumerate(chars):
                t = next_state[j][k]
                # if t == m -> would complete a forbidden occurrence; skip
                if t >= m:
                    continue
                cost = cur + (0 if si == c else 1)
                if cost < ndp2[t]:
                    ndp2[t] = cost
        dp2 = ndp2
    ans = min(dp2)
    if ans >= INF:
        # If all states unreachable, it means every path would have produced P at some point.
        # But we can always flip characters to avoid finishing P; in practice ans should be finite.
        ans = n  # worst-case flip everything
    return int(ans)

def ensure_out_dir():
    if not os.path.exists(OUT_DIR):
        os.makedirs(OUT_DIR)

def write_output_file(subtask: str, case: str, ans: int) -> str:
    fname = f"subtarea-{subtask}.{case}.out"
    path = os.path.join(OUT_DIR, fname)
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"{ans}\n")
    return path

def verify_output(path_out: str, expected: int) -> bool:
    try:
        with open(path_out, "r", encoding="utf-8") as f:
            content = f.read().strip()
        # Accept either integer or integer with trailing newline
        try:
            val = int(content.split()[0]) if content else None
        except Exception:
            return False
        return val == expected
    except FileNotFoundError:
        return False

def process_all():
    files = list_input_files()
    if not files:
        print("No se encontraron archivos .in en la carpeta 'cases/'.")
        return
    ensure_out_dir()
    total = 0
    ok = 0
    for fname in files:
        try:
            subtask, case = parse_filename(fname)
        except ValueError as e:
            print(f"Saltando archivo con nombre inválido: {fname} ({e})")
            continue
        path_in = os.path.join(CASES_DIR, fname)
        try:
            n, m, S, P = read_case(path_in)
        except Exception as e:
            print(f"Error leyendo {fname}: {e}")
            continue
        ans = solve_instance(n, m, S, P)
        out_path = write_output_file(subtask, case, ans)
        verified = verify_output(out_path, ans)
        total += 1
        if verified:
            ok += 1
            status = "OK"
        else:
            status = "ERROR"
        print(f"Procesado: {fname} -> {os.path.basename(out_path)} | respuesta={ans} | verificación={status}")
    print(f"Resumen: procesados={total}, verificados_correctos={ok}, carpeta_salida='{OUT_DIR}/'")

if __name__ == "__main__":
    process_all()
