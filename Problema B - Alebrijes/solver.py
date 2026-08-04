#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
solver.py - Procesador de archivos .in en cases/ y generador de .out

Este script recorre todos los archivos `cases/subtarea-*.in`, resuelve cada caso
contenidos en ellos (formato con t casos por archivo) y escribe el archivo
correspondiente `cases/subtarea-*.out` con una línea por caso: "SI" o "NO".

Uso:
    python3 solver.py

Notas:
- Implementa el algoritmo exacto por BFS multi‑fuente sobre intervalos [l,r].
- Sobrescribe archivos .out existentes.
- Maneja entradas malformadas de forma conservadora (escribe "NO" para el caso afectado).
"""

import os
import glob
import sys
from collections import deque
from typing import List

CASES_DIR = "cases"
PATTERN = os.path.join(CASES_DIR, "subtarea-*.in")

# ---------------------------
# Lógica de resolución por caso
# ---------------------------

def solve_case(N: int, K: int, a: List[int]) -> bool:
    """
    Devuelve True si existe una forma de ensamblar todas las piezas (SI), False en caso contrario (NO).
    Enfoque: BFS multi-fuente sobre intervalos [l,r] con suma S = sum(a[l..r]).
    Transiciones permitidas:
      - [l,r] -> [l-1,r] si l>0 y S + a[l-1] >= K
      - [l,r] -> [l,r+1] si r+1<N y S + a[r+1] >= K
    """
    if N == 0:
        return False
    if N == 1:
        return True

    # Prefijos para sumar intervalos en O(1)
    pref = [0] * (N + 1)
    for i in range(N):
        pref[i+1] = pref[i] + a[i]

    # Poda rápida: si las dos piezas más grandes no alcanzan K, imposible (no hay segundo paso)
    if N >= 2:
        s = sorted(a)
        if s[-1] + s[-2] < K:
            return False

    # visited como bytearray de tamaño N*N (index = l * N + r)
    size = N * N
    visited = bytearray(size)

    def idx(l: int, r: int) -> int:
        return l * N + r

    q = deque()

    # Inicializar con todos los intervalos unitarios [i,i]
    for i in range(N):
        p = idx(i, i)
        visited[p] = 1
        q.append((i, i))

    target = idx(0, N - 1)

    while q:
        l, r = q.popleft()
        if l == 0 and r == N - 1:
            return True
        S = pref[r+1] - pref[l]

        # expandir a la izquierda
        if l > 0 and S + a[l-1] >= K:
            ni = idx(l-1, r)
            if not visited[ni]:
                visited[ni] = 1
                if ni == target:
                    return True
                q.append((l-1, r))

        # expandir a la derecha
        if r + 1 < N and S + a[r+1] >= K:
            ni = idx(l, r+1)
            if not visited[ni]:
                visited[ni] = 1
                if ni == target:
                    return True
                q.append((l, r+1))

    return False

# ---------------------------
# Procesamiento de archivos .in -> .out
# ---------------------------

def process_file(in_path: str) -> None:
    """
    Lee un archivo .in (con t casos), resuelve cada caso y escribe el .out correspondiente.
    """
    base, _ = os.path.splitext(in_path)
    out_path = base + ".out"

    # Leer tokens
    try:
        with open(in_path, "r", encoding="utf-8") as f:
            tokens = f.read().strip().split()
    except Exception as e:
        # Si no se puede leer el archivo, no crear .out y reportar
        print(f"[ERROR] No se pudo leer {in_path}: {e}", file=sys.stderr)
        return

    if not tokens:
        # Archivo vacío -> crear .out vacío o con nada; aquí escribimos nada
        with open(out_path, "w", encoding="utf-8") as fo:
            fo.write("")  # archivo vacío
        print(f"[WARN] {in_path} está vacío. Se creó {out_path} vacío.")
        return

    it = iter(tokens)
    out_lines = []

    # Parse t
    try:
        t = int(next(it))
    except StopIteration:
        print(f"[ERROR] Formato inválido en {in_path}: falta t", file=sys.stderr)
        return
    except ValueError:
        print(f"[ERROR] Formato inválido en {in_path}: t no es entero", file=sys.stderr)
        return

    for case_no in range(t):
        # Leer N y K
        try:
            N = int(next(it))
            K = int(next(it))
        except StopIteration:
            # Malformado: no hay suficientes tokens; escribir NO para los casos faltantes
            print(f"[ERROR] Entrada truncada en {in_path} (caso {case_no+1}). Se marcará como NO.", file=sys.stderr)
            out_lines.append("NO")
            # rellenar los casos restantes con NO
            for _ in range(case_no + 1, t):
                out_lines.append("NO")
            break
        except ValueError:
            print(f"[ERROR] N o K no son enteros en {in_path} (caso {case_no+1}). Se marcará como NO.", file=sys.stderr)
            out_lines.append("NO")
            # intentar continuar leyendo pero es probable que falle; para simplicidad, rellenar con NO
            for _ in range(case_no + 1, t):
                out_lines.append("NO")
            break

        # Leer N valores a_i
        a = []
        malformed = False
        for i in range(N):
            try:
                a.append(int(next(it)))
            except StopIteration:
                print(f"[ERROR] Faltan valores a_i en {in_path} (caso {case_no+1}). Se marcará como NO.", file=sys.stderr)
                malformed = True
                break
            except ValueError:
                print(f"[ERROR] Valor a_i no entero en {in_path} (caso {case_no+1}). Se marcará como NO.", file=sys.stderr)
                malformed = True
                break

        if malformed:
            out_lines.append("NO")
            # intentar sincronizar: no hay forma fiable de sincronizar tokens, así que rellenar el resto con NO
            for _ in range(case_no + 1, t):
                out_lines.append("NO")
            break

        # Resolver el caso
        try:
            ok = solve_case(N, K, a)
            out_lines.append("SI" if ok else "NO")
        except MemoryError:
            # En caso de falta de memoria, reportar y escribir NO
            print(f"[ERROR] MemoryError al resolver {in_path} (caso {case_no+1}). Se marcará como NO.", file=sys.stderr)
            out_lines.append("NO")
        except Exception as e:
            print(f"[ERROR] Excepción al resolver {in_path} (caso {case_no+1}): {e}", file=sys.stderr)
            out_lines.append("NO")

    # Escribir archivo .out (sobrescribe si existe)
    try:
        with open(out_path, "w", encoding="utf-8") as fo:
            fo.write("\n".join(out_lines) + ("\n" if out_lines else ""))
    except Exception as e:
        print(f"[ERROR] No se pudo escribir {out_path}: {e}", file=sys.stderr)
        return

    print(f"[OK] Procesado {os.path.basename(in_path)} -> {os.path.basename(out_path)} ({len(out_lines)} casos).")

def main():
    files = sorted(glob.glob(PATTERN))
    if not files:
        print(f"No se encontraron archivos '{PATTERN}'. Asegúrate de que la carpeta '{CASES_DIR}/' existe y contiene archivos .in.", file=sys.stderr)
        return

    for path in files:
        process_file(path)

if __name__ == "__main__":
    main()
