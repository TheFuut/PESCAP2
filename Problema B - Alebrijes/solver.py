#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Solucionador basado en la lógica proporcionada (C++ -> Python).
- Procesa todos los archivos "subtarea-{subtask}.{case}.in" dentro de la carpeta "cases".
- Cada .in debe comenzar con un entero T (número de casos).
- Para cada caso se lee N K y luego N enteros a_i.
- Para cada caso se aplica la comprobación descrita:
    mx = máximo entre (a[0] + a[i]) para i != 0 y (a[N-1] + a[i]) para i != N-1
  Si mx >= K -> "SI", en caso contrario -> "NO".
- Genera un archivo .out por cada .in en la carpeta ".out/" con el mismo prefijo:
    subtarea-{subtask}.{case}.out
- Cada .out contiene una línea por caso con "SI" o "NO".
- No imprime nada por stdout.
"""

from pathlib import Path
from typing import List, Tuple

IN_DIR = Path("cases")
OUT_DIR = Path("cases")

YES = "SI"
NO = "NO"


def parse_filename(fn: str) -> Tuple[str, str]:
    """
    Espera nombres del formato: subtarea-{subtask}.{case}.in
    Devuelve (subtask, case) si coincide, o (None, None) si no.
    """
    base = Path(fn).name
    if not base.startswith("subtarea-") or not base.endswith(".in"):
        return None, None
    core = base[len("subtarea-"):-len(".in")]  # "{subtask}.{case}"
    if "." not in core:
        return None, None
    subtask, case = core.split(".", 1)
    if not (subtask.isdigit() and case.isdigit()):
        return None, None
    return subtask, case


def read_int_tokens(path: Path) -> List[int]:
    """Lee todo el archivo y devuelve la lista de tokens convertidos a int."""
    raw = path.read_bytes().split()
    try:
        return [int(x) for x in raw]
    except Exception as e:
        raise ValueError(f"Archivo {path.name} contiene tokens no enteros: {e}")


def process_file_tokens(tokens: List[int]) -> List[str]:
    """
    Interpreta tokens donde el primer entero es T y luego T instancias.
    Para cada instancia aplica la lógica descrita y devuelve la lista de resultados.
    """
    if not tokens:
        raise ValueError("Archivo vacío")
    t = tokens[0]
    if t < 0:
        raise ValueError("T negativo")
    results: List[str] = []
    idx = 1
    for _ in range(t):
        if idx + 1 >= len(tokens):
            raise ValueError("Faltan N y K para un caso")
        n = tokens[idx]; k = tokens[idx + 1]; idx += 2
        if n < 0:
            raise ValueError("N negativo")
        if idx + n > len(tokens):
            raise ValueError("Faltan a_i para un caso")
        a = tokens[idx: idx + n]; idx += n

        # Aplicar la lógica traducida del C++ proporcionado
        # Calcular mx inicializado a 0 (como en el C++ original)
        mx = 0
        if n >= 2:
            # max over a[0] + a[i] for i = 1..N-1
            base0 = a[0]
            for i in range(1, n):
                s = base0 + a[i]
                if s > mx:
                    mx = s
            # max over a[N-1] + a[i] for i = 0..N-2
            basel = a[-1]
            for i in range(0, n - 1):
                s = basel + a[i]
                if s > mx:
                    mx = s
        else:
            # n == 1: loops in C++ skip and mx remains 0
            # replicate that behavior
            mx = 0

        results.append(YES if mx >= k else NO)

    return results


def write_out(path_in: Path, subtask: str, case: str, results: List[str]) -> Path:
    """Escribe el archivo .out correspondiente en OUT_DIR y devuelve su Path."""
    OUT_DIR.mkdir(exist_ok=True)
    out_name = f"subtarea-{subtask}.{case}.out"
    out_path = OUT_DIR / out_name
    text = "\n".join(results) + ("\n" if results else "")
    out_path.write_text(text, encoding="utf-8")
    return out_path


def write_err(path_in: Path, subtask: str, case: str, message: str) -> None:
    """Escribe un archivo .err con información sobre el problema de lectura/parseo."""
    OUT_DIR.mkdir(exist_ok=True)
    err_name = f"subtarea-{subtask}.{case}.err"
    err_path = OUT_DIR / err_name
    lines = [f"IN: {path_in.name}", f"Error: {message}"]
    err_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def process_all_cases() -> None:
    """Procesa todos los archivos válidos en IN_DIR y genera .out (y .err si aplica)."""
    if not IN_DIR.is_dir():
        return

    files = sorted(IN_DIR.glob("subtarea-*.in"))
    for f in files:
        subtask, case = parse_filename(f.name)
        if subtask is None:
            # Ignorar archivos que no cumplan el patrón exacto
            continue
        try:
            tokens = read_int_tokens(f)
        except Exception as e:
            write_err(f, subtask, case, f"Lectura de tokens fallida: {e}")
            continue

        try:
            results = process_file_tokens(tokens)
        except Exception as e:
            write_err(f, subtask, case, f"Formato inválido: {e}")
            continue

        # Escribir .out con los resultados
        write_out(f, subtask, case, results)


def main() -> None:
    process_all_cases()


if __name__ == "__main__":
    main()
