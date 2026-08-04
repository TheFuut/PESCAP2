#!/usr/bin/env python3
# solver.py
# Lee todos los .in en la carpeta cases/ y genera los .out correspondientes.
# Algoritmo: ordenar por a asc, b desc; luego LIS estricta sobre b (O(N log N)).

import os
import glob
import bisect

CASES_DIR = "cases"

def solve_pairs(pairs):
    # Ordenar por a asc, y en empates por b desc
    pairs.sort(key=lambda x: (x[0], -x[1]))
    # Extraer b
    lis = []
    for _, b in pairs:
        # Para subsecuencia estrictamente creciente usamos bisect_left
        # que reemplaza el primer elemento >= b, evitando contar iguales.
        i = bisect.bisect_left(lis, b)
        if i == len(lis):
            lis.append(b)
        else:
            lis[i] = b
    return len(lis)

def process_file(path_in):
    # Leer archivo .in
    with open(path_in, "r", encoding="utf-8") as f:
        data = f.read().strip().split()
    if not data:
        return None
    it = iter(data)
    try:
        n = int(next(it))
    except StopIteration:
        return None
    pairs = []
    for _ in range(n):
        try:
            a = int(next(it)); b = int(next(it))
        except StopIteration:
            break
        pairs.append((a,b))
    ans = solve_pairs(pairs)
    return ans

def main():
    if not os.path.isdir(CASES_DIR):
        print(f"Directorio '{CASES_DIR}' no encontrado.")
        return

    in_files = sorted(glob.glob(os.path.join(CASES_DIR, "subtarea-*.in")))
    if not in_files:
        print("No se encontraron archivos .in en la carpeta 'cases/'.")
        return

    for path_in in in_files:
        ans = process_file(path_in)
        if ans is None:
            print(f"Saltando {path_in}: formato inválido o vacío.")
            continue
        base = os.path.splitext(os.path.basename(path_in))[0]
        path_out = os.path.join(CASES_DIR, base + ".out")
        with open(path_out, "w", encoding="utf-8") as f:
            f.write(str(ans) + "\n")
        print(f"Wrote {path_out}")

if __name__ == "__main__":
    main()
