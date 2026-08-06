#!/usr/bin/env python3
# Generador de casos de prueba para el problema "Alebrijes"
# - Crea carpeta cases/
# - Genera archivos con nombres exactos: subtarea-{subtask}.{case}.in
# - Determinista (semilla fija)
# - Incluye variedad de casos y mezcla SI/NO
# - Respeta límites y suma total de N <= 1e6

import os
import random
from pathlib import Path
from typing import List, Tuple

SEED = 123456789
random.seed(SEED)

OUT_DIR = Path("cases")
OUT_DIR.mkdir(exist_ok=True)

# Límites globales
MAX_TOTAL_N = 10**6
GLOBAL_N_MIN = 2
GLOBAL_N_MAX = 10**6
A_MIN = 1
A_MAX = 10**9
K_MIN = 1
K_MAX = 10**9

# Número de archivos por subtarea (según enunciado)
CASES_PER_SUBTASK = {
    1: 10,
    2: 15,
    3: 25,
    4: 25,
}

# Mantener suma total de N para no exceder MAX_TOTAL_N
remaining_N_budget = MAX_TOTAL_N

# Helpers para construir instancias con respuesta conocida por construcción.
def make_yes_by_end(N: int, K: int, place_left: bool = True, pattern: str = "random") -> List[int]:
    """
    Construye un arreglo que garantiza respuesta SI:
    - Si place_left True, a[0] >= K (entonces siempre se puede empezar por la izquierda y propagar).
    - Si place_left False, a[-1] >= K.
    pattern controla la distribución del resto.
    """
    arr = [None] * N
    big = max(K, K + 1)  # >= K
    if place_left:
        arr[0] = big
    else:
        arr[-1] = big

    def fill_random(low, high):
        return [random.randint(low, high) for _ in range(N)]

    if pattern == "all_ge_k":
        # todos >= K
        arr = [big] * N
    elif pattern == "equal":
        val = random.randint(1, max(1, K))
        arr = [val] * N
        if place_left:
            arr[0] = big
        else:
            arr[-1] = big
    elif pattern == "increasing":
        base = random.randint(1, max(1, K//2))
        seq = [base + i for i in range(N)]
        if place_left:
            seq[0] = big
        else:
            seq[-1] = big
        arr = seq
    elif pattern == "decreasing":
        base = random.randint(1, max(1, K//2))
        seq = [base + (N - i) for i in range(N)]
        if place_left:
            seq[0] = big
        else:
            seq[-1] = big
        arr = seq
    elif pattern == "alternating":
        small = max(1, K//10)
        large = max(K, K//2 + 1)
        seq = [large if i % 2 == 0 else small for i in range(N)]
        if place_left:
            seq[0] = big
        else:
            seq[-1] = big
        arr = seq
    else:
        # random small values but ensure the chosen end is big
        low = 1
        high = max(1, K - 1)
        for i in range(N):
            if arr[i] is None:
                arr[i] = random.randint(low, high)
    return arr

def make_no_by_ends_blocked(N: int, K: int, pattern: str = "random") -> List[int]:
    """
    Construye un arreglo que garantiza respuesta NO por construcción:
    - Ambos extremos no pueden sumarse con ninguna otra pieza para alcanzar K.
      Es decir, for all j != 0, a0 + a_j < K and for all j != N-1, aN-1 + a_j < K.
    - Para lograrlo, fijamos extremos muy pequeños y el resto también lo suficientemente pequeño.
    """
    # Elegimos extremos small_e y interior small_i tal que small_e + max_interior < K
    # Para seguridad, ponemos max_interior = K-2 and small_e = 1 so sum = K-1 < K
    if K <= 2:
        # Si K muy pequeño, es difícil bloquear; en ese caso hacemos NO con N=2 y suma<K
        if N == 2:
            a0 = 1
            a1 = max(1, K - 1)  # sum < K
            return [a0, a1]
        # si K<=2 y N>2, hacemos interiores zeros (1) and K large? but K small; fallback:
        # make interior all 1 and ends 1 but set K=3 artificially? Instead, set K to 3 by caller.
        pass

    small_end = 1
    interior_max = max(1, K - 2)  # ensure small_end + interior_max = K-1 < K
    arr = [None] * N
    arr[0] = small_end
    arr[-1] = small_end

    if pattern == "all_small":
        arr = [1] * N
        arr[0] = small_end
        arr[-1] = small_end
    elif pattern == "many_small_one_big":
        # Put one big in interior but still ensure big + small_end < K
        big = interior_max
        for i in range(1, N-1):
            arr[i] = big
    elif pattern == "increasing":
        # increasing but capped so ends can't pair
        seq = [1 + i % (interior_max) for i in range(N)]
        seq[0] = small_end
        seq[-1] = small_end
        arr = seq
    else:
        # random small values <= interior_max
        for i in range(1, N-1):
            arr[i] = random.randint(1, interior_max)
    return arr

def make_edge_case_two(N: int, K: int, want_yes: bool) -> List[int]:
    # N==2 special
    if want_yes:
        # ensure a1+a2 >= K
        a1 = random.randint(1, K)
        a2 = max(1, K - a1)
        # maybe increase to ensure >=K
        if a1 + a2 < K:
            a2 = K - a1
        return [a1, a2]
    else:
        # ensure a1+a2 < K
        a1 = 1
        a2 = max(1, K - 1)
        if a1 + a2 >= K:
            a2 = max(1, K - 1)
            if a1 + a2 >= K:
                a1 = 1
                a2 = 1
        return [a1, a2]

# Función para escribir un archivo .in con T casos
def write_case_file(filename: Path, tests: List[Tuple[int,int,List[int]]]):
    """
    tests: lista de (N, K, arr)
    """
    with open(filename, "w", encoding="utf-8") as f:
        f.write(str(len(tests)) + "\n")
        for N, K, arr in tests:
            f.write(f"{N} {K}\n")
            f.write(" ".join(str(x) for x in arr) + "\n")

# Generadores por subtarea
def gen_subtask_1(case_id: int) -> Tuple[Path, int]:
    """
    Subtarea 1: T = 1, N <= 10. Generar 10 archivos.
    """
    global remaining_N_budget
    T = 1
    # N pequeño
    N = random.randint(2, 10)
    if remaining_N_budget - N < 0:
        N = 2
    remaining_N_budget -= N

    # Alternar SI/NO por case_id
    want_yes = (case_id % 2 == 1)
    K = random.randint(1, 50)
    if N == 2:
        arr = make_edge_case_two(N, K, want_yes)
    else:
        if want_yes:
            # choose patterns
            pattern = random.choice(["random", "equal", "alternating", "increasing"])
            place_left = random.choice([True, False])
            arr = make_yes_by_end(N, K, place_left=place_left, pattern=pattern)
        else:
            pattern = random.choice(["random", "all_small", "increasing"])
            arr = make_no_by_ends_blocked(N, K, pattern=pattern)
    filename = OUT_DIR / f"subtarea-1.{case_id}.in"
    write_case_file(filename, [(N, K, arr)])
    return filename, N

def gen_subtask_2(case_id: int) -> Tuple[Path, int]:
    """
    Subtarea 2: N <= 100. Generate varied T and cases.
    """
    global remaining_N_budget
    # Choose T variations: sometimes max (we'll use 15), sometimes small
    T_options = [1, 3, 5, 10, 15]
    T = random.choice(T_options)
    tests = []
    totalN = 0
    for t in range(T):
        N = random.randint(2, 100)
        if remaining_N_budget - N < 0:
            N = 2
        remaining_N_budget -= N
        totalN += N
        want_yes = random.choice([True, False])
        K = random.randint(1, 200)
        if N == 2:
            arr = make_edge_case_two(N, K, want_yes)
        else:
            if want_yes:
                pattern = random.choice(["random", "equal", "alternating", "increasing", "decreasing"])
                place_left = random.choice([True, False])
                arr = make_yes_by_end(N, K, place_left=place_left, pattern=pattern)
            else:
                pattern = random.choice(["random", "all_small", "many_small_one_big"])
                arr = make_no_by_ends_blocked(N, K, pattern=pattern)
        tests.append((N, K, arr))
    filename = OUT_DIR / f"subtarea-2.{case_id}.in"
    write_case_file(filename, tests)
    return filename, totalN

def gen_subtask_3(case_id: int) -> Tuple[Path, int]:
    """
    Subtarea 3: a_i, K <= 100. N up to maybe 1000 but keep reasonable.
    """
    global remaining_N_budget
    T = random.choice([1, 5, 10, 20, 50])
    tests = []
    totalN = 0
    for t in range(T):
        N = random.randint(2, 500)
        if remaining_N_budget - N < 0:
            N = 2
        remaining_N_budget -= N
        totalN += N
        want_yes = random.choice([True, False])
        K = random.randint(1, 100)
        if N == 2:
            arr = make_edge_case_two(N, K, want_yes)
        else:
            if want_yes:
                pattern = random.choice(["all_ge_k", "equal", "alternating", "increasing"])
                place_left = random.choice([True, False])
                arr = make_yes_by_end(N, K, place_left=place_left, pattern=pattern)
            else:
                pattern = random.choice(["all_small", "many_small_one_big", "random"])
                arr = make_no_by_ends_blocked(N, K, pattern=pattern)
        # cap values to <=100
        arr = [min(100, max(1, x)) for x in arr]
        tests.append((N, K, arr))
    filename = OUT_DIR / f"subtarea-3.{case_id}.in"
    write_case_file(filename, tests)
    return filename, totalN

def gen_subtask_4(case_id: int) -> Tuple[Path, int]:
    """
    Subtarea 4: Sin restricciones adicionales. Incluir casos grandes.
    """
    global remaining_N_budget
    # We want some files with large N, some with small.
    # Decide N based on remaining budget and randomness
    # Ensure at least 2
    max_allowed = min(200000, remaining_N_budget - (CASES_PER_SUBTASK[4] - case_id) * 2)
    if max_allowed < 2:
        max_allowed = 2
    # For variety, sometimes pick very large, sometimes moderate
    choice = random.random()
    if choice < 0.08 and max_allowed >= 200000:
        N = 200000
    elif choice < 0.25 and max_allowed >= 100000:
        N = random.randint(50000, min(100000, max_allowed))
    else:
        N = random.randint(2, min(50000, max_allowed))
    if remaining_N_budget - N < 0:
        N = 2
    remaining_N_budget -= N

    # Choose T: sometimes large T (but ensure total N budget)
    T = random.choice([1, 2, 5, 10, 50])
    tests = []
    usedN = 0
    for t in range(T):
        # distribute N across T parts
        if t == T - 1:
            Ni = N - usedN
            if Ni < 2:
                Ni = 2
        else:
            # allocate at least 2
            max_part = max(2, (N - usedN) - 2*(T - t - 1))
            Ni = random.randint(2, max_part)
        usedN += Ni

        want_yes = random.choice([True, False])
        # K choose relative to Ni to create interesting cases
        # sometimes very large K to force NO, sometimes small to allow YES
        K_choice = random.random()
        if K_choice < 0.2:
            K = random.randint(1, 10)
        elif K_choice < 0.6:
            K = random.randint(1, 10**6)
        else:
            K = random.randint(1, 10**9)

        if Ni == 2:
            arr = make_edge_case_two(Ni, K, want_yes)
        else:
            if want_yes:
                pattern = random.choice(["random", "equal", "alternating", "increasing", "all_ge_k", "decreasing"])
                place_left = random.choice([True, False])
                arr = make_yes_by_end(Ni, K, place_left=place_left, pattern=pattern)
            else:
                pattern = random.choice(["random", "all_small", "many_small_one_big", "increasing"])
                arr = make_no_by_ends_blocked(Ni, K, pattern=pattern)

        # Add special crafted subcases
        special = random.random()
        if special < 0.05:
            # single huge in middle, others small
            big = min(10**9, max(K, 10**8))
            mid = Ni // 2
            for i in range(Ni):
                arr[i] = 1
            arr[mid] = big
            # ensure want_yes depends on whether an end can pair with big
            # but we keep construction as-is (may be YES or NO depending on K)
        elif special < 0.1:
            # many equal values
            val = random.randint(1, min(10**9, max(1, K)))
            arr = [val] * Ni
        # ensure bounds
        arr = [min(A_MAX, max(A_MIN, x)) for x in arr]
        tests.append((Ni, K, arr))

    filename = OUT_DIR / f"subtarea-4.{case_id}.in"
    write_case_file(filename, tests)
    return filename, N

# Main generator
def main():
    print("Generador de casos para 'Alebrijes' - iniciando...")
    generated = []
    total_files = sum(CASES_PER_SUBTASK.values())
    file_count = 0

    # Subtask 1
    for i in range(1, CASES_PER_SUBTASK[1] + 1):
        filename, usedN = gen_subtask_1(i)
        generated.append((filename, usedN))
        file_count += 1
        print(f"Generado: {filename} (N={usedN})")

    # Subtask 2
    for i in range(1, CASES_PER_SUBTASK[2] + 1):
        filename, usedN = gen_subtask_2(i)
        generated.append((filename, usedN))
        file_count += 1
        print(f"Generado: {filename} (sum N={usedN})")

    # Subtask 3
    for i in range(1, CASES_PER_SUBTASK[3] + 1):
        filename, usedN = gen_subtask_3(i)
        generated.append((filename, usedN))
        file_count += 1
        print(f"Generado: {filename} (sum N={usedN})")

    # Subtask 4
    for i in range(1, CASES_PER_SUBTASK[4] + 1):
        filename, usedN = gen_subtask_4(i)
        generated.append((filename, usedN))
        file_count += 1
        print(f"Generado: {filename} (N budget used={usedN})")

    total_N_used = sum(n for _, n in generated)
    print("\nResumen final:")
    print(f"  Archivos generados: {len(generated)}")
    print(f"  Suma total de N usada: {total_N_used} (límite {MAX_TOTAL_N})")
    print(f"  Directorio de salida: {OUT_DIR.resolve()}")
    print("Generación completada.")

if __name__ == "__main__":
    main()
