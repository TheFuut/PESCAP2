# Academia de danza

Sasha y Judith han abierto una academia de danza inspirada en las tradiciones de México. En cada audición llegan bailarines con mucha energía, pero la presentación final exige una secuencia muy precisa para que el número se vea elegante. No basta con que los bailarines sean buenos por separado. También importa cómo se acomodan dentro de la coreografía.

Cada bailarín tiene dos cualidades. La primera representa su dominio técnico y la segunda representa su coordinación con el grupo. Para que dos bailarines puedan estar uno después del otro en la presentación, ambos valores deben crecer de manera estricta. Judith insiste en que la secuencia debe verse natural, como si cada paso fuera superando al anterior sin romper la armonía del espectáculo.

# Descripción

Te dan $N$ bailarines, y cada uno tiene dos enteros $a_i$ y $b_i$. Debes elegir el mayor número posible de bailarines para formar una secuencia válida. Una secuencia es válida si, al ordenar a los bailarines elegidos en el orden de la presentación, sus valores $a$ y $b$ aumentan estrictamente de izquierda a derecha.

Sasha y Judith pueden elegir a los bailarines que quieran, pero una vez elegidos, deben acomodarlos para que la presentación sea válida.

# Entrada

La primera línea contiene un entero $N$, que indica el número de bailarines que llegaron a la academia.

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

Se ordenan los bailarines por $a$ ascendente y, en empates, por $b$ descendente. La lista queda con $(2, 3)$, $(2, 2)$, $(3, 4)$, $(4, 1)$ y $(5, 5)$.

La subsecuencia estrictamente creciente más larga sobre $b$ es $(2, 2)$, $(3, 4)$ y $(5, 5)$, por lo que la respuesta es $3$.

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

La mejor idea vuelve a ser ordenar por $a$ ascendente y, en empates, por $b$ descendente. Después se calcula la subsecuencia estrictamente creciente más larga sobre $b$.

Una secuencia máxima válida es $(1,1)$, $(2,3)$, $(3,4)$, $(4,6)$, $(5,7)$, así que la respuesta es $5$.

||end

# Consideraciones

- $1 \le N \le 2 × 10^5$
- $1 \le a_i, b_i \le 10^9$
- Puede haber bailarines con valores repetidos

# Subtareas

- Subtarea 1 (20 puntos): $N \le 2000$
- Subtarea 2 (20 puntos): $N \le 10^4$
- Subtarea 3 (25 puntos): $N \le 5 \times 10^4$ y todos los $a_i$ son distintos
- Subtarea 4 (35 puntos): Sin restricciones adicionales.
