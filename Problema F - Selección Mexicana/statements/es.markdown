# Selección Mexicana

Después de analizar el rendimiento de cientos de futbolistas, el director técnico de la Selección Mexicana ha reducido la lista a $N$ candidatos para disputar el siguiente torneo internacional.

Sin embargo, la convocatoria no depende únicamente del nivel de cada jugador. Existen diversas condiciones deportivas y de convivencia:

- algunos jugadores sólo aceptan asistir si otro también es convocado;
- algunos futbolistas no pueden coincidir en la misma convocatoria;
- en ciertos casos, al menos uno de dos jugadores debe formar parte del equipo.

El cuerpo técnico quiere saber si existe alguna convocatoria que satisfaga todas las condiciones impuestas.

Tu tarea es determinar si es posible formar una convocatoria válida.

# Descripción

Se tienen $N$ jugadores numerados del $1$ al $N$. Cada jugador puede ser o no convocado.

También se proporcionan $M$ restricciones. Cada restricción pertenece a uno de los siguientes tipos:

- $1 \ A \ B$ - Si el jugador $A$ es convocado, entonces el jugador $B$ también debe ser convocado.
- $2 \ A \ B$ - Los jugadores $A$ y $B$ no pueden ser convocados al mismo tiempo.
- $3 \ A \ B$ - Al menos uno de los jugadores $A$ o $B$ debe ser convocado.

Determina si es posible anunciar una convocatoria que cumpla con todas las condiciones.

# Entrada

La primera línea contiene dos enteros $N$ y $M$, que representan el número de jugadores y el número de condiciones, respectivamente.

Cada una de las siguientes $M$ líneas describe una condición mediante tres enteros $T, A$ y $B$, donde $T$ indica el tipo de condición y $A$ y $B$ los jugadores.

# Salida

Si existe al menos una convocatoria que satisfaga todas las condiciones, imprime `SI`. En caso contrario, imprime `NO`.

# Ejemplos

||input

3 3
1 1 2
2 2 3
3 1 3

||output

SI

||description

Una convocatoria posible es:

- jugador 1 convocado;
- jugador 2 convocado;
- jugador 3 no convocado.

Todas las restricciones se satisfacen.

||input

2 4
1 1 2
1 2 1
3 1 2
2 1 2

|| output

NO

||description

Las dos primeras restricciones obligan a que $1$ y $2$ tengan el mismo estado (si $1$ entonces $2$, y si $2$ entonces $1$). La tercera exige que al menos uno esté convocado, por lo que ambos deberían estar convocados; la cuarta prohíbe que ambos estén convocados. No existe asignación que satisfaga todas las condiciones.

||end

# Consideraciones

- $2 \le N \le 2 \times 10^5$
- $1 \le M \le 4 \times 10^5$
- $1 \le T \le 3$
- $1 \le A, B \le N$
- $A$ es distinta de $B$

# Subtareas

- Subtarea 1 (10 puntos): $N \le 20$
- Subtarea 2 (20 puntos): Sólo hay restricciones de tipo $2$.
- Subtarea 3 (20 puntos): $N, M \le 5000$
- Subtarea 4 (50 puntos): Sin restricciones adicionales.
