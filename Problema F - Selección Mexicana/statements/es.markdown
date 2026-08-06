# Selección Mexicana

Después de meses de seguimiento en la liga local y en el extranjero, el director técnico de la Selección Mexicana está listo para anunciar la convocatoria final para el próximo torneo internacional.

La lista de candidatos ya está definida, pero elaborar la convocatoria no es tan sencillo como elegir a los mejores jugadores. El cuerpo técnico debe tomar en cuenta compromisos adquiridos con algunos futbolistas, conflictos dentro del vestidor y decisiones estratégicas sobre ciertas posiciones.

Antes de publicar la lista definitiva, el entrenador quiere comprobar que todas esas condiciones puedan cumplirse al mismo tiempo. Si alguna de ellas entra en conflicto con las demás, será imposible anunciar una convocatoria válida.

Tu tarea es determinar si existe alguna forma de elegir a los jugadores convocados respetando todas las condiciones establecidas.

# Descripción

Se tienen $N$ jugadores numerados del $1$ al $N$. Cada jugador puede ser **convocado** o **no convocado**.

Además, se proporcionan $M$ condiciones. Cada una pertenece a uno de los siguientes tipos:

- $1 \ A \ B$ - Si el jugador $A$ es convocado, entonces el jugador $B$ también debe ser convocado.
- $2 \ A \ B$ - Los jugadores $A$ y $B$ no pueden ser convocados al mismo tiempo.
- $3 \ A \ B$ - Al menos uno de los jugadores $A$ o $B$ debe ser convocado.

Determina si es posible anunciar una convocatoria que cumpla con todas las condiciones.

# Entrada

La primera línea contiene dos enteros $N$ y $M$, que representan el número de jugadores y el número de condiciones, respectivamente.

Cada una de las siguientes $M$ líneas contiene tres enteros $T, A$ y $B$, donde $T$ indica el tipo de condición y $A$ y $B$ representan a los jugadores involucrados.

# Salida

Imprime `SI` si existe al menos una convocatoria que satisfaga todas las condiciones. En caso contrario, imprime `NO`.

# Ejemplos

||input

3 3
1 1 2
2 2 3
3 1 3

||output

SI

||description

Una posible convocatoria incluye a los jugadores $1$ y $2$, mientras que el jugador $3$ queda fuera de la lista.

El jugador $1$ cumple con la condición de estar acompañado por el $2$, los jugadores $2$ y $3$ no coinciden en la convocatoria y, además, entre los jugadores $1$ y $3$ hay al menos uno convocado. Por lo tanto, todas las condiciones se satisfacen.

||input

2 4
1 1 2
1 2 1
3 1 2
2 1 2

|| output

NO

||description

Las dos primeras condiciones hacen que los jugadores $1$ y $2$ siempre deban compartir el mismo destino: ambos son convocados o ambos quedan fuera. Sin embargo, otra condición obliga a que al menos uno aparezca en la lista, mientras que la última prohíbe que coincidan en la convocatoria. No existe ninguna forma de satisfacer todas las condiciones simultáneamente.

||end

# Consideraciones

- $2 \le N \le 2 \times 10^5$
- $1 \le M \le 4 \times 10^5$
- $1 \le T \le 3$
- $1 \le A, B \le N$
- $A \neq B$

# Subtareas

- Subtarea 1 (10 puntos): $N \le 20$
- Subtarea 2 (20 puntos): Sólo hay restricciones de tipo $2$.
- Subtarea 3 (20 puntos): $N, M \le 5000$
- Subtarea 4 (50 puntos): Sin restricciones adicionales.
