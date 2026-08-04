#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen.py - Generador de archivos .in para la versión actualizada del problema "Alebrijes"

Esta versión adapta el generador a la nueva especificación:
- Ahora cada archivo de entrada contiene t casos de prueba.
- Formato de cada archivo:
    t
    N K
    a1 a2 ... aN
    (repetir para cada caso)
- Restricciones globales por archivo: la suma de todos los N en el archivo no excede 5000.
- Subtareas con límites adicionales en N por caso:
    Subtarea 1: N <= 300
    Subtarea 2: N <= 3000
    Subtarea 3: N <= 5000
- El script crea la carpeta `cases/` si no existe y sobrescribe archivos existentes.
- Usa una semilla fija para reproducibilidad.
- Genera casos variados y útiles (límites, patrones, aleatorios, casos engañosos, etc.)
- Organización en funciones: gen_subtask_1/2/3 y auxiliares.

Nombres de archivos:
    subtarea-{subtask}.{case}.in
donde {subtask} ∈ {1,2,3} y {case} comienza en 1 para cada subtarea.

NOTA: Este generador **solo** crea archivos .in. No genera .out.
"""

import os
import random
from typing import List, Tuple

# ---------------------------
# Configuración global
# ---------------------------
OUT_DIR = "cases"
SEED = 12345
random.seed(SEED)

# Cantidad de archivos por subtarea (manteniendo la organización previa)
FILES_PER_SUBTASK = {1: 20, 2: 15, 3: 25}

# Límites por subtarea (actualizados según la nueva declaración)
SUBTASK_LIMITS = {
    1: {"N_min": 1, "N_max": 300, "a_min": 1, "a_max": 10**9, "K_min": 1, "K_max": 10**9},
    2: {"N_min": 1, "N_max": 3000, "a_min": 1, "a_max": 10**9, "K_min": 1, "K_max": 10**9},
    3: {"N_min": 1, "N_max": 5000, "a_min": 1, "a_max": 10**9, "K_min": 1, "K_max": 10**9},
}

# Restricción global por archivo: suma de N en el archivo <= 5000
SUM_N_LIMIT_PER_FILE = 5000

# ---------------------------
# Utilidades
# ---------------------------

def ensure_out_dir():
    os.makedirs(OUT_DIR, exist_ok=True)

def clamp(val: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, val))

def validate_case_limits(subtask: int, N: int, K: int, arr: List[int]) -> None:
    """Valida que un caso cumple las restricciones de la subtarea."""
    limits = SUBTASK_LIMITS[subtask]
    if not (limits["N_min"] <= N <= limits["N_max"]):
        raise ValueError(f"N fuera de rango para subtarea {subtask}: {N}")
    if not (limits["K_min"] <= K <= limits["K_max"]):
        raise ValueError(f"K fuera de rango para subtarea {subtask}: {K}")
    if len(arr) != N:
        raise ValueError(f"Longitud de arreglo incorrecta: esperado {N}, obtenido {len(arr)}")
    for x in arr:
        if not (limits["a_min"] <= x <= limits["a_max"]):
            raise ValueError(f"Valor ai fuera de rango para subtarea {subtask}: {x}")

def write_input_file(subtask: int, file_no: int, cases: List[Tuple[int,int,List[int]]]) -> None:
    """Escribe un archivo .in con varios casos. Sobrescribe si existe."""
    # Validar suma de N
    totalN = sum(N for (N, K, arr) in cases)
    if totalN > SUM_N_LIMIT_PER_FILE:
        raise ValueError(f"Suma de N en archivo excede {SUM_N_LIMIT_PER_FILE}: {totalN}")
    # Validar cada caso
    for (N, K, arr) in cases:
        validate_case_limits(subtask, N, K, arr)
    filename = os.path.join(OUT_DIR, f"subtarea-{subtask}.{file_no}.in")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(str(len(cases)) + "\n")
        for (N, K, arr) in cases:
            f.write(f"{N} {K}\n")
            f.write(" ".join(str(x) for x in arr) + "\n")

# ---------------------------
# Generadores de casos individuales (patrones)
# ---------------------------

def seq_increasing(N: int, a_min: int, a_max: int) -> List[int]:
    if N == 1:
        return [random.randint(a_min, a_max)]
    span = max(1, a_max - a_min + 1)
    if span >= N:
        vals = sorted(random.sample(range(a_min, a_max + 1), k=N))
        return vals
    return [a_min + i for i in range(N)]

def seq_decreasing(N: int, a_min: int, a_max: int) -> List[int]:
    s = seq_increasing(N, a_min, a_max)
    s.reverse()
    return s

def seq_all_equal(N: int, value: int) -> List[int]:
    return [value] * N

def seq_many_repeats(N: int, distinct: int, a_min: int, a_max: int) -> List[int]:
    distinct = max(1, min(distinct, N))
    pool = [random.randint(a_min, a_max) for _ in range(distinct)]
    arr = [random.choice(pool) for _ in range(N)]
    random.shuffle(arr)
    return arr

def seq_random(N: int, a_min: int, a_max: int) -> List[int]:
    return [random.randint(a_min, a_max) for _ in range(N)]

def seq_min_values(N: int, a_min: int) -> List[int]:
    return [a_min] * N

def seq_max_values(N: int, a_max: int) -> List[int]:
    return [a_max] * N

def seq_near_sum_max(N: int, a_min: int, a_max: int) -> List[int]:
    if N <= 3:
        return seq_random(N, a_min, a_max)
    big1 = a_max
    big2 = max(a_min, a_max // 2)
    rest = [random.randint(a_min, max(a_min, a_max // 10)) for _ in range(N - 2)]
    arr = [big1, big2] + rest
    random.shuffle(arr)
    return arr

def seq_tricky_for_greedy(N: int, a_min: int, a_max: int) -> List[int]:
    if N == 1:
        return [random.randint(a_min, a_max)]
    large1 = max(a_min, a_max // 2)
    large2 = large1 + random.randint(0, max(1, a_max // 10))
    smalls = [random.randint(a_min, max(a_min, a_max // 20)) for _ in range(max(0, N - 2))]
    arr = [large1, large2] + smalls
    random.shuffle(arr)
    return arr

# ---------------------------
# Construcción de conjuntos de casos por archivo
# ---------------------------

def build_cases_for_file(subtask: int, target_totalN: int) -> List[Tuple[int,int,List[int]]]:
    """
    Construye una lista de casos cuyo total de N sea <= target_totalN (y preferiblemente cercano).
    Se mezclan patrones para lograr variedad.
    """
    limits = SUBTASK_LIMITS[subtask]
    remaining = target_totalN
    cases = []

    # Queremos entre 3 y 30 casos por archivo, dependiendo del tamaño permitido
    max_cases = min(30, max(1, target_totalN // 10))
    num_cases = random.randint(3, max_cases) if target_totalN >= 10 else 1

    # Distribuir tamaños: generar tamaños aleatorios pero respetando límites y la suma
    for i in range(num_cases):
        # Si queda poco espacio, crear un pequeño caso
        max_allowed_N = min(limits["N_max"], remaining - (num_cases - i - 1) * limits["N_min"])
        if max_allowed_N < limits["N_min"]:
            break
        # Elegir N: preferir variedad (a veces grande, a veces pequeño)
        if remaining > limits["N_max"] and random.random() < 0.2:
            N = random.randint(max(1, limits["N_max"] // 2), limits["N_max"])
        else:
            # elegir N entre 1 y max_allowed_N, pero no demasiado pequeño siempre
            N = random.randint(limits["N_min"], max(1, min(max_allowed_N, max(5, max_allowed_N // 4))))
        N = clamp(N, limits["N_min"], max_allowed_N)
        # Elegir patrón aleatoriamente
        pattern = random.random()
        if pattern < 0.08:
            arr = seq_min_values(N, limits["a_min"])
        elif pattern < 0.16:
            arr = seq_max_values(N, limits["a_max"])
        elif pattern < 0.28:
            val = random.randint(limits["a_min"], min(limits["a_max"], 1000))
            arr = seq_all_equal(N, val)
        elif pattern < 0.40:
            arr = seq_increasing(N, limits["a_min"], min(limits["a_max"], 100000))
        elif pattern < 0.52:
            arr = seq_decreasing(N, limits["a_min"], min(limits["a_max"], 100000))
        elif pattern < 0.66:
            arr = seq_many_repeats(N, distinct=max(1, N//10), a_min=limits["a_min"], a_max=min(limits["a_max"], 10000))
        elif pattern < 0.80:
            arr = seq_tricky_for_greedy(N, limits["a_min"], min(limits["a_max"], 10**7))
        else:
            arr = seq_random(N, limits["a_min"], min(limits["a_max"], 10**7))

        # Elegir K con varios criterios para cubrir casos interesantes
        # Algunas opciones: K=1, K small, K equal to an element, K equal to sum of two elements,
        # K slightly above some element, K near total sum, K impossible (greater than sum of two largest)
        choice = random.random()
        if choice < 0.08:
            K = 1
        elif choice < 0.18:
            K = random.randint(1, max(1, min(100, max(arr))))
        elif choice < 0.30:
            K = random.choice(arr)
        elif choice < 0.44 and N >= 2:
            s = sorted(arr, reverse=True)
            K = s[0] + s[1]
        elif choice < 0.58:
            total = sum(arr)
            K = random.randint(1, max(1, min(total, limits["K_max"])))
        elif choice < 0.72:
            # K slightly above sum of two largest to create NO cases
            s = sorted(arr, reverse=True)
            if N >= 2:
                K = min(limits["K_max"], s[0] + s[1] + random.randint(1, max(1, s[0]//2)))
            else:
                K = min(limits["K_max"], arr[0] + random.randint(0, 10))
        else:
            # K near maximum possible (but clamped)
            total = sum(arr)
            K = min(limits["K_max"], max(1, total - random.randint(0, max(0, total//10))))
        K = clamp(K, limits["K_min"], limits["K_max"])

        cases.append((N, K, arr))
        remaining -= N
        if remaining < limits["N_min"]:
            break

    # If we have remaining capacity, optionally add one more small random case
    if remaining >= limits["N_min"]:
        # add one small case to use leftover capacity
        N = min(remaining, min(limits["N_max"], max(1, remaining)))
        arr = seq_random(N, limits["a_min"], min(limits["a_max"], 10**6))
        K = random.randint(1, min(sum(arr), limits["K_max"]))
        cases.append((N, K, arr))
    # Final safety: ensure totalN <= SUM_N_LIMIT_PER_FILE
    totalN = sum(N for (N, K, arr) in cases)
    if totalN > SUM_N_LIMIT_PER_FILE:
        # Trim last cases until within limit
        while cases and sum(N for (N, K, arr) in cases) > SUM_N_LIMIT_PER_FILE:
            cases.pop()
    return cases

# ---------------------------
# Generadores por subtarea (archivos)
# ---------------------------

def gen_subtask(subtask: int, files_count: int):
    """Genera `files_count` archivos para la subtarea dada."""
    limits = SUBTASK_LIMITS[subtask]
    ensure_out_dir()
    for file_no in range(1, files_count + 1):
        # Decidir target total N para este archivo: entre 50 y SUM_N_LIMIT_PER_FILE
        # pero respetando subtarea: if subtarea small, we can keep smaller totals
        if subtask == 1:
            target = random.randint(50, min(800, SUM_N_LIMIT_PER_FILE))
        elif subtask == 2:
            target = random.randint(200, min(2000, SUM_N_LIMIT_PER_FILE))
        else:
            target = random.randint(500, SUM_N_LIMIT_PER_FILE)
        # Build cases ensuring per-case N <= limits["N_max"] and total <= target
        cases = build_cases_for_file(subtask, target)
        # As a safety, if no cases were built (shouldn't happen), create a trivial one
        if not cases:
            N = limits["N_min"]
            arr = seq_random(N, limits["a_min"], min(limits["a_max"], 1000))
            K = random.randint(1, min(sum(arr), limits["K_max"]))
            cases = [(N, K, arr)]
        # Write file
        write_input_file(subtask, file_no, cases)
    print(f"Subtarea {subtask}: generados {files_count} archivos en '{OUT_DIR}/'.")

# ---------------------------
# Main
# ---------------------------

def main():
    ensure_out_dir()
    print("Generando archivos .in con semilla fija:", SEED)
    gen_subtask(1, FILES_PER_SUBTASK[1])
    gen_subtask(2, FILES_PER_SUBTASK[2])
    gen_subtask(3, FILES_PER_SUBTASK[3])
    print("Generación completada. Revisa la carpeta 'cases/' para los archivos .in.")

if __name__ == "__main__":
    main()
