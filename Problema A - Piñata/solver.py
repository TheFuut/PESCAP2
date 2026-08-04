#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Solver para "¡Ya cayó la piñata!"
- Si existe la carpeta "cases", procesa todos los archivos "subtarea-*.in"
  y genera un archivo por cada uno con la misma base y extensión ".out"
  que contiene únicamente la respuesta ("Dulces para todos" o "Sin dulces").
- Si no existe "cases", lee una única instancia desde stdin y escribe la
  respuesta en stdout.
El programa no imprime mensajes adicionales.
"""

from pathlib import Path
import sys

YES = "Dulces para todos"
NO = "Sin dulces"


def resultado_desde_tokens(tokens) -> str:
    """Calcula el resultado (YES/NO) a partir de una lista/iterable de tokens."""
    it = iter(tokens)
    try:
        n = int(next(it))
        k = int(next(it))
    except StopIteration:
        return NO
    total = 0
    for _ in range(n):
        try:
            total += int(next(it))
        except StopIteration:
            break
    return YES if total >= k else NO


def procesar_archivo_entrada(path: Path) -> str:
    """Lee un archivo de entrada y devuelve la respuesta como cadena."""
    data = path.read_bytes().split()
    return resultado_desde_tokens(data)


def escribir_salida_archivo(path_out: Path, resultado: str) -> None:
    """Escribe el resultado en path_out (una sola línea, con salto de línea)."""
    path_out.write_text(resultado + "\n", encoding="utf-8")


def procesar_carpeta_cases(cases_dir: Path) -> None:
    """Procesa todos los archivos subtarea-*.in y genera .out correspondientes."""
    files = sorted(cases_dir.glob("subtarea-*.in"))
    for f in files:
        resultado = procesar_archivo_entrada(f)
        out_path = f.with_suffix(".out")
        escribir_salida_archivo(out_path, resultado)


def procesar_stdin_stdout() -> None:
    """Lee stdin y escribe la respuesta en stdout."""
    data = sys.stdin.buffer.read().split()
    resultado = resultado_desde_tokens(data)
    sys.stdout.write(resultado + "\n")


def main() -> None:
    cases_dir = Path("cases")
    if cases_dir.is_dir():
        procesar_carpeta_cases(cases_dir)
    else:
        procesar_stdin_stdout()


if __name__ == "__main__":
    main()
