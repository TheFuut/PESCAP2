# Ya cayó la piñata

## Historia

En una típica fiesta mexicana llegó el momento favorito de todos: ¡romper la piñata! Los niños ya están formados con los ojos bien abiertos, esperando que comiencen a caer los dulces. Algunos incluso ya eligieron cuál será el primer dulce que intentarán recoger.

Cada niño da exactamente un golpe a la piñata con una fuerza determinada. La pobre piñata intenta resistir tanto como puede, pero si la suma de todas las fuerzas alcanza o supera su resistencia, finalmente se romperá y comenzará la lluvia de dulces. Si logra aguantar todos los golpes, los niños seguramente pedirán otra ronda.

## Descripción

Dados el número de golpes $N$, la resistencia $K$ de una piñata y la fuerza de cada uno de los $N$ golpes, determina si la suma de todas las fuerzas es suficiente para romperla.

## Entrada

La primera línea contiene dos enteros $N$ y $K$, donde $N$ representa el número de golpes y $K$ la resistencia de la piñata.

La segunda línea contiene $N$ enteros $a_1, a_2, \dots, a_N$, donde $a_i$ representa la fuerza del $i$-ésimo golpe.

## Salida

Imprime una única línea: `Dulces para todos` si la suma de las fuerzas es al menos $K$; en caso contrario, imprime `Sin dulces`.

## Ejemplo

| Entrada | Salida | Descripción |
| :--- | :--- | :--- |
| 5 20<br>3 4 6 2 8 | ¡Dulces para todos! | La suma de las fuerzas es<br>$$3+4+6+2+8=23.$$Como $23 \ge 20$, la piñata se rompe, por lo que la respuesta es `¡Dulces para todos!`.|

## Consideraciones

- $1 \le N \le 10^5$
- $1 \le K \le 10^9$
- $1 \le a_i \le 10^4$

## Subtareas

- Subtarea 1 (20 puntos): $N \le 10$
- Subtarea 2 (30 puntos): $N \le 1000$
- Subtarea 3 (50 puntos): Sin restricciones adicionales.

## Nota

El comité organizador no se hace responsable por empujones, codazos o disputas ocasionadas durante la recolección de dulces.
