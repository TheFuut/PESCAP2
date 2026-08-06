#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador determinista de casos de prueba para el problema:
"Renata y los ademanes"

Crea archivos en la carpeta `cases/` con nombres:
  subtarea-{subtask}.{case}.in

Cada archivo contiene:
  N M
  S
  P

El generador es determinista (semilla fija).
Imprime un resumen de los archivos generados.
"""

import os
import random
from typing import Tuple

SEED = 12345
OUT_DIR = "cases"

# Número de casos por subtarea (según enunciado)
CASES_PER_SUBTASK = {
    1: 10,
    2: 15,
    3: 10,
    4: 25,
    5: 15,
}

# Límites globales
N_MAX = 2 * 10**5
M_MAX = 400

random.seed(SEED)


def ensure_out_dir():
    if not os.path.exists(OUT_DIR):
        os.makedirs(OUT_DIR)


def write_case(subtask: int, idx: int, N: int, M: int, S: str, P: str):
    filename = f"subtarea-{subtask}.{idx}.in"
    path = os.path.join(OUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"{N} {M}\n")
        f.write(S + "\n")
        f.write(P + "\n")
    print(f"Generado: {filename} (N={N}, M={M})")


def alternating_string(n: int, start_char: str = "<") -> str:
    other = ">" if start_char == "<" else "<"
    return "".join(start_char if i % 2 == 0 else other for i in range(n))


def block_string(n: int, block_size: int, start_char: str = "<") -> str:
    s = []
    cur = start_char
    i = 0
    while i < n:
        take = min(block_size, n - i)
        s.append(cur * take)
        cur = ">" if cur == "<" else "<"
        i += take
    return "".join(s)


def random_string(n: int, p_left: float = 0.5) -> str:
    return "".join("<" if random.random() < p_left else ">" for _ in range(n))


def repeat_pattern(pattern: str, n: int) -> str:
    # repeat pattern to length n (may cut last repetition)
    return (pattern * ((n // len(pattern)) + 2))[:n]


def make_case_varieties(N: int, M: int, variant: str) -> Tuple[str, str]:
    """
    Devuelve (S, P) según la variante solicitada.
    variant puede ser:
      'alternating', 'alternating_start_right', 'blocks_small', 'blocks_large',
      'random_balanced', 'random_skewed_left', 'random_skewed_right',
      'S_all_left', 'S_all_right', 'P_all_left', 'P_all_right',
      'overlapping', 'P_longer', 'P_equal', 'P_one', 'S_small_random'
    """
    if variant == "alternating":
        S = alternating_string(N, "<")
        P = alternating_string(M, "<")
    elif variant == "alternating_start_right":
        S = alternating_string(N, ">")
        P = alternating_string(M, ">")
    elif variant == "blocks_small":
        S = block_string(N, max(1, M // 2 or 1), "<")
        P = "<" * M  # pattern of same char to force overlaps
    elif variant == "blocks_large":
        S = block_string(N, max(1, N // 5), "<")
        P = ">" * M
    elif variant == "random_balanced":
        S = random_string(N, 0.5)
        P = random_string(M, 0.5)
    elif variant == "random_skewed_left":
        S = random_string(N, 0.7)
        P = random_string(M, 0.6)
    elif variant == "random_skewed_right":
        S = random_string(N, 0.3)
        P = random_string(M, 0.4)
    elif variant == "S_all_left":
        S = "<" * N
        P = random_string(M, 0.5)
    elif variant == "S_all_right":
        S = ">" * N
        P = random_string(M, 0.5)
    elif variant == "P_all_left":
        S = random_string(N, 0.5)
        P = "<" * M
    elif variant == "P_all_right":
        S = random_string(N, 0.5)
        P = ">" * M
    elif variant == "overlapping":
        # create S with long runs to create many overlapping occurrences of P
        base = "<" * max(1, M - 1)
        S = repeat_pattern(base, N)
        P = "<" * M
    elif variant == "P_longer":
        # P longer than S (M > N)
        S = random_string(N, 0.5)
        P = random_string(M, 0.5)
    elif variant == "P_equal":
        S = random_string(N, 0.5)
        P = random_string(M, 0.5)
    elif variant == "P_one":
        S = random_string(N, 0.5)
        P = "<" if random.random() < 0.5 else ">"
    elif variant == "S_small_random":
        S = random_string(N, 0.5)
        P = random_string(M, 0.5)
    elif variant == "repeat_short_pattern":
        pat = random.choice(["<>", "><", "<<<", ">>>", "<><"])
        S = repeat_pattern(pat, N)
        P = pat * (M // len(pat) + 1)
        P = P[:M]
    else:
        # fallback
        S = random_string(N, 0.5)
        P = random_string(M, 0.5)

    # Safety: ensure lengths
    S = S[:N].ljust(N, "<")
    P = P[:M].ljust(M, "<")
    return S, P


def gen_subtask_1():
    """Subtarea 1: N <= 20, M <= 20 (10 casos)"""
    sub = 1
    cnt = CASES_PER_SUBTASK[sub]
    idx = 1
    variants = [
        ("small_alt", 5, 3, "alternating"),
        ("small_alt2", 7, 3, "alternating_start_right"),
        ("all_left_small", 10, 3, "S_all_left"),
        ("all_right_small", 12, 1, "S_all_right"),
        ("overlap_small", 8, 3, "overlapping"),
        ("random_small", 15, 5, "random_balanced"),
        ("P_longer", 5, 7, "P_longer"),  # M > N
        ("P_one_cases", 6, 1, "P_one"),
        ("blocks_small", 20, 4, "blocks_small"),
        ("repeat_short", 18, 5, "repeat_short_pattern"),
    ]
    for name, N, M, variant in variants[:cnt]:
        S, P = make_case_varieties(N, M, variant)
        write_case(sub, idx, N, M, S, P)
        idx += 1


def gen_subtask_2():
    """Subtarea 2: N <= 1000, M <= 50 (15 casos)"""
    sub = 2
    cnt = CASES_PER_SUBTASK[sub]
    idx = 1
    # mix of edge and random
    cases = []
    # small N, small M
    cases.append((50, 3, "alternating"))
    cases.append((100, 1, "P_one"))
    cases.append((200, 50, "random_balanced"))  # M at upper bound for subtask
    cases.append((500, 10, "blocks_large"))
    cases.append((1000, 20, "random_skewed_left"))
    cases.append((999, 50, "P_equal"))
    cases.append((250, 60 if 60 <= M_MAX else 50, "random_balanced"))  # ensure M<=M_MAX
    # crafted to create many overlapping occurrences
    cases.append((300, 3, "overlapping"))
    cases.append((400, 4, "repeat_short_pattern"))
    cases.append((1000, 1, "S_all_right"))
    cases.append((800, 2, "alternating"))
    cases.append((700, 7, "blocks_small"))
    cases.append((123, 5, "random_skewed_right"))
    cases.append((321, 15, "random_balanced"))
    cases.append((100, 101 if 101 <= M_MAX else 50, "P_longer"))  # M > N scenario if possible

    for N, M, variant in cases[:cnt]:
        # clamp M to allowed for this subtask (<=50) and global M_MAX
        M = min(M, 50, M_MAX)
        S, P = make_case_varieties(N, M, variant)
        write_case(sub, idx, N, M, S, P)
        idx += 1


def gen_subtask_3():
    """Subtarea 3: M <= 20 (10 casos). N can be large."""
    sub = 3
    cnt = CASES_PER_SUBTASK[sub]
    idx = 1
    cases = []
    # include very large N
    cases.append((N_MAX, 1, "P_one"))
    cases.append((N_MAX, 2, "alternating"))
    cases.append((200000, 20, "overlapping"))
    cases.append((150000, 20, "S_all_left"))
    cases.append((100000, 5, "random_balanced"))
    cases.append((50000, 3, "repeat_short_pattern"))
    cases.append((25000, 4, "blocks_large"))
    cases.append((12345, 7, "random_skewed_right"))
    cases.append((9999, 20, "P_all_left"))
    cases.append((1, 1, "P_one"))  # minimal edge

    for N, M, variant in cases[:cnt]:
        M = min(M, 20, M_MAX)
        S, P = make_case_varieties(N, M, variant)
        write_case(sub, idx, N, M, S, P)
        idx += 1


def gen_subtask_4():
    """Subtarea 4: M <= 100 (25 casos)."""
    sub = 4
    cnt = CASES_PER_SUBTASK[sub]
    idx = 1
    cases = []

    # Mix many sizes and patterns
    sizes = [10, 20, 50, 100, 200, 500, 1000, 5000, 10000, 20000]
    variants = [
        "alternating", "alternating_start_right", "blocks_small", "blocks_large",
        "random_balanced", "random_skewed_left", "random_skewed_right",
        "S_all_left", "S_all_right", "P_all_left", "P_all_right",
        "overlapping", "repeat_short_pattern", "P_one"
    ]

    # create combinations
    for s in sizes:
        for v in variants:
            m = random.randint(1, min(100, M_MAX))
            cases.append((min(s, N_MAX), m, v))
            if len(cases) >= cnt:
                break
        if len(cases) >= cnt:
            break

    # If not enough, add random ones
    while len(cases) < cnt:
        N = random.randint(1, min(20000, N_MAX))
        M = random.randint(1, min(100, M_MAX))
        variant = random.choice(variants)
        cases.append((N, M, variant))

    for N, M, variant in cases[:cnt]:
        M = min(M, 100, M_MAX)
        S, P = make_case_varieties(N, M, variant)
        write_case(sub, idx, N, M, S, P)
        idx += 1


def gen_subtask_5():
    """Subtarea 5: Sin restricciones adicionales (15 casos)."""
    sub = 5
    cnt = CASES_PER_SUBTASK[sub]
    idx = 1
    cases = []

    # include extreme large N and M up to 400
    cases.append((N_MAX, 400, "random_balanced"))
    cases.append((N_MAX, 400, "S_all_left"))
    cases.append((N_MAX, 1, "P_one"))
    cases.append((200000, 400, "overlapping"))
    cases.append((150000, 300, "repeat_short_pattern"))
    cases.append((100000, 200, "random_skewed_left"))
    cases.append((50000, 100, "blocks_large"))
    cases.append((40000, 399, "random_balanced"))
    cases.append((30000, 400, "P_all_right"))
    cases.append((25000, 250, "alternating"))
    cases.append((20000, 201, "P_longer"))  # maybe M > N if chosen
    cases.append((10000, 400, "blocks_small"))
    cases.append((5000, 50, "random_balanced"))
    cases.append((1234, 400, "random_skewed_right"))
    cases.append((2, 2, "alternating"))

    for N, M, variant in cases[:cnt]:
        M = min(M, M_MAX)
        # allow M > N in some cases intentionally (P_longer)
        if variant == "P_longer" and M <= N:
            # force M > N if possible
            M = min(M + 5, M_MAX)
            if M <= N:
                M = min(N + 1, M_MAX)
        S, P = make_case_varieties(N, M, variant)
        write_case(sub, idx, N, M, S, P)
        idx += 1


def main():
    ensure_out_dir()
    print("Iniciando generación de casos (semilla fija = {}).".format(SEED))
    gen_subtask_1()
    gen_subtask_2()
    gen_subtask_3()
    gen_subtask_4()
    gen_subtask_5()
    print("Generación completada. Archivos guardados en la carpeta 'cases/'.")


if __name__ == "__main__":
    main()
