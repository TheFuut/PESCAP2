# Academia de danza

Sasha y Judith han abierto una academia dedicada a preservar las danzas tradicionales de México. Después de varias semanas de ensayos, llegó el momento de elegir a los bailarines que participarán en la presentación principal del festival.

Cada bailarín posee dos cualidades. La primera mide su dominio técnico de los pasos y la segunda representa qué tan bien logra sincronizarse con el resto del grupo. Judith quiere que la coreografía transmita una sensación de progreso constante, por lo que cada bailarín que aparezca después de otro debe superar al anterior en ambas cualidades. Si alguno de los dos valores deja de aumentar, la armonía de la presentación se rompe.

# Descripción

Se tienen $N$ bailarines. El bailarín $i$ está descrito por dos enteros $a_i$ y $b_i$, que representan su dominio técnico y su coordinación, respectivamente.

Puedes elegir cualquier subconjunto de bailarines y acomodarlos en el orden que desees para la presentación.

Una secuencia es **válida** si, para cada par de bailarines consecutivos en la presentación, tanto el dominio técnico como la coordinación aumentan de manera estricta.

Determina el mayor número de bailarines que pueden formar una secuencia válida.

# Entrada

La primera línea contiene un entero $N$, el número de bailarines que participaron en la audición.

Cada una de las siguientes $N$ líneas contiene dos enteros $a_i$ y $b_i$, donde $a_i$ representa el dominio técnico del bailarín y $b_i$ representa su coordinación con el grupo.

# Salida

Imprime un solo entero, el máximo número de bailarines que pueden formar una secuencia válida.

# Ejemplos

||input

5
2 3
2 2
3 4
4 1
5 5

||output

3

||description

Aunque existen dos bailarines con el mismo dominio técnico $(a = 2)$, ambos no pueden aparecer en la misma secuencia porque el dominio debe aumentar estrictamente entre bailarines consecutivos.

La mejor presentación posible utiliza tres bailarines, por ejemplo

$$(2, 2) → (3, 4) → (5, 5),$$

donde ambas cualidades aumentan en cada transición. No existe ninguna secuencia válida con cuatro bailarines.

||input

6
1 1
2 5
2 3
3 4
4 6
5 7

||output

5

||description

Los bailarines con dominio técnico igual a 2 no pueden participar simultáneamente en la misma secuencia válida. Para obtener la presentación más larga es necesario elegir únicamente uno de ellos.

Una secuencia óptima está formada por

$$(1, 1) → (2, 3) → (3, 4) → (4,6) → (5, 7),$$

por lo que la respuesta es $5$.

||end

# Consideraciones

- $1 \le N \le 2 × 10^5$
- $1 \le a_i, b_i \le 10^9$
- Los valores de $a_i$ y $b_i$ pueden repetirse.

# Subtareas

- Subtarea 1 (20 puntos): $N \le 2000$
- Subtarea 2 (20 puntos): $N \le 10^4$
- Subtarea 3 (25 puntos): $N \le 5 \times 10^4$ y todos los $a_i$ son distintos
- Subtarea 4 (35 puntos): Sin restricciones adicionales.
