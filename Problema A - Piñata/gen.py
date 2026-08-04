#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de casos para el problema "¡Ya cayó la piñata!"
Cumple los requisitos solicitados:
 - Crea carpeta cases/ si no existe.
 - Genera archivos con nombre exacto: subtarea-{subtask}.{case}.in
 - Genera archivos para las subtareas 1, 2 y 3.
 - Determinista usando semilla fija.
 - Funciones separadas por subtarea.
 - Imprime resumen por consola con N, K, suma y respuesta esperada.
"""

import os
import random
from pathlib import Path
from typing import List

# Semilla fija para determinismo
SEED = 12345
random.seed(SEED)

OUT_DIR = Path("cases")
OUT_DIR.mkdir(exist_ok=True)

# Límites del problema
A_MIN = 1
A_MAX = 10_000
K_MIN = 1
K_MAX = 10**9
N_GLOBAL_MAX = 100_000

# Mensajes esperados
YES_MSG = "Dulces para todos"
NO_MSG = "Sin dulces"


def escribir_caso(subtask: int, case_num: int, N: int, K: int, arr: List[int]) -> None:
    """Escribe un archivo de caso con el formato requerido y muestra resumen."""
    filename = OUT_DIR / f"subtarea-{subtask}.{case_num}.in"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"{N} {K}\n")
        f.write(" ".join(map(str, arr)) + "\n")

    suma = sum(arr)
    resultado = YES_MSG if suma >= K else NO_MSG
    print(f"Generado {filename}: N={N}, K={K}, suma={suma}, Resultado esperado: {resultado}")


def distribuir_suma(N: int, objetivo: int) -> List[int]:
    """
    Distribuye 'objetivo' en N enteros entre A_MIN y A_MAX inclusive.
    Lanza ValueError si no es posible.
    Método determinista (usa random pero con semilla global).
    """
    if objetivo < N * A_MIN or objetivo > N * A_MAX:
        raise ValueError(f"No se puede distribuir {objetivo} en {N} elementos con límites [{A_MIN},{A_MAX}]")
    arr = [A_MIN] * N
    restante = objetivo - N * A_MIN
    # Distribuir de forma pseudoaleatoria pero determinista
    for i in range(N):
        if restante <= 0:
            break
        add = min(A_MAX - A_MIN, restante)
        take = random.randrange(0, add + 1)
        arr[i] += take
        restante -= take
    i = N - 1
    while restante > 0 and i >= 0:
        can = A_MAX - arr[i]
        put = min(can, restante)
        arr[i] += put
        restante -= put
        i -= 1
    if restante != 0:
        raise RuntimeError("Error al distribuir la suma restante")
    return arr


# ---------- Generadores auxiliares de distribuciones ----------

def todos_min(N: int) -> List[int]:
    return [A_MIN] * N


def todos_max(N: int) -> List[int]:
    return [A_MAX] * N


def todos_iguales(N: int, val: int) -> List[int]:
    val = max(A_MIN, min(A_MAX, val))
    return [val] * N


def aleatorio(N: int, low=A_MIN, high=A_MAX) -> List[int]:
    return [random.randint(low, high) for _ in range(N)]


def un_golpe_grande(N: int, big_value: int = A_MAX) -> List[int]:
    arr = [A_MIN] * N
    idx = random.randrange(0, N)
    arr[idx] = max(A_MIN, min(A_MAX, big_value))
    return arr


def muchos_pequenos(N: int, small_value: int = 1) -> List[int]:
    return [small_value] * N


def crecientes(N: int) -> List[int]:
    if N == 1:
        return [A_MIN]
    step = max(1, (A_MAX - A_MIN) // (N - 1))
    arr = [min(A_MAX, A_MIN + i * step) for i in range(N)]
    return [max(A_MIN, min(A_MAX, x)) for x in arr]


def decrecientes(N: int) -> List[int]:
    return list(reversed(crecientes(N)))


def alternada(N: int, low=A_MIN, high=A_MAX) -> List[int]:
    arr = []
    for i in range(N):
        arr.append(low if i % 2 == 0 else high)
    return arr


# ---------- Subtarea 1 (N <= 10) ----------

def generar_subtarea_1():
    """
    Genera 10 casos para la subtarea 1 (N <= 10).
    Cubre casos borde y aleatorios pequeños.
    """
    subtask = 1
    casos = []
    # Diseñar 10 casos variados con N <= 10
    casos.append(("minimos_pequeno", 1, None))        # N=1, todos min
    casos.append(("maximos_pequeno", 1, None))       # N=1, todos max
    casos.append(("todos_min", 5, None))             # todos mínimos
    casos.append(("todos_max", 5, None))             # todos máximos
    casos.append(("iguales", 6, 100))                # todos iguales
    casos.append(("aleatorio", 7, None))             # aleatorio
    casos.append(("un_grande", 8, None))             # un golpe grande
    casos.append(("muchos_pequenos", 10, None))      # muchos pequeños
    casos.append(("exacto_suma", 9, None))           # suma == K
    casos.append(("suma_menos_uno", 10, None))       # suma == K - 1

    case_num = 1
    yes_count = 0
    no_count = 0
    desired_yes = 5
    desired_no = 5

    for tag, N, param in casos:
        N = min(N, 10)
        if tag == "minimos_pequeno":
            arr = todos_min(N)
            suma = sum(arr)
            # K = 1 to force YES
            K = 1
            if suma >= K:
                yes_count += 1
            else:
                no_count += 1
        elif tag == "maximos_pequeno":
            arr = todos_max(N)
            suma = sum(arr)
            # K grande to force YES (since max)
            K = suma
            yes_count += 1
        elif tag == "todos_min":
            arr = todos_min(N)
            suma = sum(arr)
            # Alternar respuesta
            if no_count < desired_no:
                K = suma + 1
                no_count += 1
            else:
                K = suma
                yes_count += 1
        elif tag == "todos_max":
            arr = todos_max(N)
            suma = sum(arr)
            if yes_count < desired_yes:
                K = suma
                yes_count += 1
            else:
                K = suma + 1
                no_count += 1
        elif tag == "iguales":
            val = param if param is not None else 50
            arr = todos_iguales(N, val)
            suma = sum(arr)
            # Hacer K = suma +/-1 para variar
            if yes_count < desired_yes:
                K = suma
                yes_count += 1
            else:
                K = suma + 1
                no_count += 1
        elif tag == "aleatorio":
            arr = aleatorio(N)
            suma = sum(arr)
            # Elegir K cercano a suma
            if yes_count < desired_yes:
                K = max(K_MIN, suma - random.randint(0, 20))
                if suma >= K:
                    yes_count += 1
                else:
                    no_count += 1
            else:
                K = suma + random.randint(1, 20)
                no_count += 1
        elif tag == "un_grande":
            arr = un_golpe_grande(N, big_value=A_MAX)
            for i in range(N):
                if arr[i] != A_MAX:
                    arr[i] = random.randint(1, 5)
            suma = sum(arr)
            if yes_count < desired_yes:
                K = suma
                yes_count += 1
            else:
                K = suma + 1
                no_count += 1
        elif tag == "muchos_pequenos":
            arr = muchos_pequenos(N, small_value=1)
            suma = sum(arr)
            K = suma + random.randint(1, 10)
            no_count += 1
        elif tag == "exacto_suma":
            objetivo = random.randint(N * A_MIN, min(N * A_MAX, N * 100))
            arr = distribuir_suma(N, objetivo)
            suma = sum(arr)
            K = suma
            yes_count += 1
        elif tag == "suma_menos_uno":
            objetivo = random.randint(N * A_MIN, min(N * A_MAX, N * 100))
            arr = distribuir_suma(N, objetivo)
            suma = sum(arr)
            K = max(K_MIN, suma - 1)
            no_count += 1
        else:
            arr = aleatorio(N)
            suma = sum(arr)
            K = suma
            yes_count += 1

        K = max(K_MIN, min(K_MAX, K))
        escribir_caso(subtask, case_num, N, K, arr)
        case_num += 1


# ---------- Subtarea 2 (N <= 1000) ----------

def generar_subtarea_2():
    """
    Genera 10 casos para la subtarea 2 (N <= 1000).
    Mezcla casos aleatorios y borde, intentando balancear respuestas.
    """
    subtask = 2
    casos = []
    # Caso 1: todos mínimos, N pequeño
    casos.append(("todos_min", 5, None))
    # Caso 2: todos máximos, N pequeño
    casos.append(("todos_max", 7, None))
    # Caso 3: valores iguales (medio)
    casos.append(("iguales", 10, 500))
    # Caso 4: completamente aleatorio
    casos.append(("aleatorio", 50, None))
    # Caso 5: un golpe muy grande entre pequeños
    casos.append(("un_grande", 20, None))
    # Caso 6: muchos pequeños (todos 1) con K grande -> Sin dulces
    casos.append(("muchos_pequenos", 100, None))
    # Caso 7: crecientes
    casos.append(("crecientes", 200, None))
    # Caso 8: decrecientes
    casos.append(("decrecientes", 200, None))
    # Caso 9: alternada
    casos.append(("alternada", 201, None))
    # Caso 10: caso exacto suma == K (usar distribuir_suma)
    casos.append(("exacto", 300, None))

    case_num = 1
    desired_yes = 5
    desired_no = 5
    yes_count = 0
    no_count = 0

    for tag, N, param in casos:
        N = min(N, 1000)
        if tag == "todos_min":
            arr = todos_min(N)
            suma = sum(arr)
            if no_count < desired_no:
                K = suma + 1
                no_count += 1
            else:
                K = suma
                yes_count += 1
        elif tag == "todos_max":
            arr = todos_max(N)
            suma = sum(arr)
            if yes_count < desired_yes:
                K = suma
                yes_count += 1
            else:
                K = suma + 1
                no_count += 1
        elif tag == "iguales":
            val = param if param is not None else 500
            arr = todos_iguales(N, val)
            suma = sum(arr)
            if suma - 1 >= K_MIN and no_count < desired_no:
                K = suma - 1
                no_count += 1
            else:
                K = suma
                yes_count += 1
        elif tag == "aleatorio":
            arr = aleatorio(N)
            suma = sum(arr)
            if yes_count < desired_yes:
                K = max(K_MIN, suma - random.randint(0, 1000))
                if K <= suma:
                    yes_count += 1
                else:
                    no_count += 1
            else:
                K = suma + random.randint(1, 1000)
                no_count += 1
        elif tag == "un_grande":
            arr = un_golpe_grande(N, big_value=A_MAX)
            for i in range(N):
                if arr[i] == A_MAX:
                    continue
                arr[i] = random.randint(1, 5)
            suma = sum(arr)
            if yes_count < desired_yes:
                K = suma
                yes_count += 1
            else:
                K = suma + 1
                no_count += 1
        elif tag == "muchos_pequenos":
            arr = muchos_pequenos(N, small_value=1)
            suma = sum(arr)
            K = suma + random.randint(1, 1000)
            no_count += 1
        elif tag == "crecientes":
            arr = crecientes(N)
            suma = sum(arr)
            if no_count < desired_no:
                K = suma + 1
                no_count += 1
            else:
                K = suma
                yes_count += 1
        elif tag == "decrecientes":
            arr = decrecientes(N)
            suma = sum(arr)
            if yes_count < desired_yes:
                K = suma - 1 if suma - 1 >= K_MIN else suma
                if K <= suma:
                    yes_count += 1
                else:
                    no_count += 1
            else:
                K = suma + 1
                no_count += 1
        elif tag == "alternada":
            arr = alternada(N)
            suma = sum(arr)
            choice = random.choice([0, -1, 1])
            if choice == 0:
                K = suma
                yes_count += 1
            elif choice == -1 and suma - 1 >= K_MIN:
                K = suma - 1
                no_count += 1
            else:
                K = suma + 1
                no_count += 1
        elif tag == "exacto":
            objetivo = min(N * A_MAX, max(N * A_MIN, random.randint(N, N * A_MAX)))
            arr = distribuir_suma(N, objetivo)
            suma = sum(arr)
            K = suma
            yes_count += 1
        else:
            arr = aleatorio(N)
            suma = sum(arr)
            K = suma
            yes_count += 1

        K = max(K_MIN, min(K_MAX, K))
        escribir_caso(subtask, case_num, N, K, arr)
        case_num += 1


# ---------- Subtarea 3 (sin restricciones adicionales) ----------

def generar_subtarea_3():
    """
    Genera 15 casos para la subtarea 3.
    Incluye varios casos con N = 100000 para rendimiento.
    Cubre distribuciones y condiciones límite.
    """
    subtask = 3
    casos = []
    casos.append(("N_max_aleatorio", N_GLOBAL_MAX, None))
    casos.append(("N_max_todos_min", N_GLOBAL_MAX, None))
    casos.append(("N_max_todos_max", N_GLOBAL_MAX, None))
    casos.append(("N_max_un_grande", N_GLOBAL_MAX, None))
    casos.append(("N_max_muchos_pequenos", N_GLOBAL_MAX, None))
    casos.append(("N_med_aleatorio", 50000, None))
    casos.append(("crecientes", 10000, None))
    casos.append(("decrecientes", 10000, None))
    casos.append(("alternada", 99999, None))
    casos.append(("exacto_grande", 100000, None))
    casos.append(("exacto_K_minus_1", 1000, None))
    casos.append(("exacto_K_plus_1", 1000, None))
    casos.append(("K_muy_pequeno", 50, None))
    casos.append(("K_muy_grande", 100000, None))
    casos.append(("mezcla_varios", 12345, None))

    case_num = 1
    yes_count = 0
    no_count = 0
    desired_yes = 8
    desired_no = 7

    for tag, N, param in casos:
        N = min(N, N_GLOBAL_MAX)
        if tag == "N_max_aleatorio":
            arr = aleatorio(N)
            suma = sum(arr)
            if yes_count < desired_yes:
                K = max(K_MIN, suma - random.randint(0, 100000))
                yes_count += 1
            else:
                K = suma + random.randint(1, 100000)
                no_count += 1
        elif tag == "N_max_todos_min":
            arr = todos_min(N)
            suma = sum(arr)
            K = suma + random.randint(1, 1000)
            no_count += 1
        elif tag == "N_max_todos_max":
            arr = todos_max(N)
            suma = sum(arr)
            K = suma
            yes_count += 1
        elif tag == "N_max_un_grande":
            arr = [random.randint(1, 5) for _ in range(N)]
            idx = random.randrange(0, N)
            arr[idx] = A_MAX
            suma = sum(arr)
            if yes_count < desired_yes:
                K = suma
                yes_count += 1
            else:
                K = suma + 1
                no_count += 1
        elif tag == "N_max_muchos_pequenos":
            arr = [1] * N
            suma = sum(arr)
            K = suma + random.randint(1, 10000)
            no_count += 1
        elif tag == "N_med_aleatorio":
            arr = aleatorio(N)
            suma = sum(arr)
            if yes_count < desired_yes:
                K = suma
                yes_count += 1
            else:
                K = suma + random.randint(1, 50000)
                no_count += 1
        elif tag == "crecientes":
            arr = crecientes(N)
            suma = sum(arr)
            if yes_count < desired_yes:
                K = max(K_MIN, suma - 1)
                yes_count += 1
            else:
                K = suma + 1
                no_count += 1
        elif tag == "decrecientes":
            arr = decrecientes(N)
            suma = sum(arr)
            if no_count < desired_no:
                K = suma + 1
                no_count += 1
            else:
                K = suma
                yes_count += 1
        elif tag == "alternada":
            arr = alternada(N)
            suma = sum(arr)
            if random.choice([True, False]):
                K = suma
                yes_count += 1
            else:
                K = suma + 1
                no_count += 1
        elif tag == "exacto_grande":
            objetivo = N * A_MAX
            arr = todos_max(N)
            suma = sum(arr)
            K = suma
            yes_count += 1
        elif tag == "exacto_K_minus_1":
            objetivo = min(N * A_MAX, max(N * A_MIN, random.randint(N, N * A_MAX)))
            arr = distribuir_suma(N, objetivo)
            suma = sum(arr)
            K = max(K_MIN, suma - 1)
            no_count += 1
        elif tag == "exacto_K_plus_1":
            objetivo = min(N * A_MAX, max(N * A_MIN, random.randint(N, N * A_MAX)))
            arr = distribuir_suma(N, objetivo)
            suma = sum(arr)
            K = suma + 1
            no_count += 1
        elif tag == "K_muy_pequeno":
            arr = aleatorio(N)
            suma = sum(arr)
            K = random.randint(1, 2)
            if suma >= K:
                yes_count += 1
            else:
                no_count += 1
        elif tag == "K_muy_grande":
            arr = aleatorio(N)
            suma = sum(arr)
            K = min(K_MAX, N * A_MAX + random.randint(0, 1000000))
            if suma >= K:
                yes_count += 1
            else:
                no_count += 1
        elif tag == "mezcla_varios":
            arr = []
            for i in range(N):
                arr.append(A_MAX if i % 2 == 0 else A_MIN)
            suma = sum(arr)
            if yes_count < desired_yes:
                K = suma
                yes_count += 1
            else:
                K = suma + 1
                no_count += 1
        else:
            arr = aleatorio(N)
            suma = sum(arr)
            K = suma
            yes_count += 1

        K = max(K_MIN, min(K_MAX, K))
        escribir_caso(subtask, case_num, N, K, arr)
        case_num += 1


# ---------- Función principal ----------

def main():
    print("Inicio de generación de casos (semilla fija = {})".format(SEED))
    print("Generando subtarea 1 (10 casos, N <= 10)...")
    generar_subtarea_1()
    print("\nGenerando subtarea 2 (10 casos, N <= 1000)...")
    generar_subtarea_2()
    print("\nGenerando subtarea 3 (15 casos, sin restricciones adicionales)...")
    generar_subtarea_3()
    print("\nGeneración completada. Archivos escritos en:", OUT_DIR.resolve())


if __name__ == "__main__":
    main()
