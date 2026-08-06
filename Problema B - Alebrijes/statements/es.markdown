# Alebrijes

En los talleres donde se elaboran los alebrijes, cada figura comienza como un conjunto de piezas de madera talladas por separado. Antes de pintarlas y decorarlas, los artesanos deben ir uniéndolas poco a poco hasta formar una sola pieza. Sin embargo, no cualquier unión es posible: la madera sólo logra adherirse cuando ambas piezas reúnen la energía suficiente.

Don Aurelio ha colocado todas las piezas sobre su mesa de trabajo formando una fila. Como dicta la tradición, nunca puede tomar una pieza del centro directamente; siempre debe comenzar por una de las piezas que se encuentran en alguno de los extremos de la mesa. Ahora quiere saber si será posible unir todas las piezas hasta obtener un único alebrije.

## Descripción

Don Aurelio tiene $N$ piezas acomodadas en una fila, donde la pieza $i$ posee una energía de $a_i$.

Mientras exista más de una pieza sobre la mesa, puede tomar una pieza que se encuentre en el extremo izquierdo o en el extremo derecho de la fila y unirla con cualquier otra pieza que aún permanezca sobre la mesa.

Dos piezas sólo pueden unirse si la suma de sus energías es al menos $K$. Cuando esto ocurre, ambas desaparecen y son reemplazadas por una nueva pieza cuya energía es la suma de las dos. La nueva pieza ocupa el lugar de la pieza que fue tomada desde el extremo de la mesa.

Tu tarea es determinar si existe alguna forma de unir todas las piezas hasta obtener una sola.

## Entrada

La primera línea contiene un entero $T$, el número de casos de prueba.

Cada caso de prueba consiste en una línea con dos enteros $N$ y $K$, seguida de una línea con $N$ enteros $a_1, a_2, \ldots, a_N$, donde $a_i$ representa la energía de la $i$-ésima pieza.

## Salida

Para cada caso de prueba, imprime una línea con `SI` si es posible obtener una única pieza. En caso contrario, imprime `NO`.

## Ejemplo

||input
3
4 10
8 4 9 2
5 12
5 4 7 3 10
4 10
1 2 3 4

||output
SI
SI
NO

||description
En el primer caso, Don Aurelio puede tomar la pieza de energía $8$, que se encuentra en un extremo, y unirla con la pieza de energía $4$. La nueva pieza tendrá energía $12$. Ahora la mesa cuenta con las piezas $[12, 9, 2]$. Don Aurelio puede escoger las piezas con energías $9$ y $2$ y juntarlas para formar una única pieza con energía $11$. La mesa ahora es $[12, 11]$. Ya sólo falta juntar estas piezas restantes y así ensamblar el alebrije.

En el segundo caso también es posible comenzar uniendo una pieza situada en un extremo con otra del interior, y continuar el proceso hasta completar el ensamblaje.

En el último caso, ninguna pieza situada en un extremo puede realizar una primera unión válida. Como el proceso nunca puede comenzar, la respuesta es `NO`.

||end

## Consideraciones

- $1 \le T \le 100$
- $2 \le N \le 10^6$
- $1 \le a_i, K \le 10^9$
- La suma de todos los valores de $N$ no excede $10^6$.

## Subtareas

- Subtarea 1 (10 puntos): $T = 1$ y $N \le 10$.
- Subtarea 2 (15 puntos): $N \le 100$.
- Subtarea 3 (25 puntos): $a_i \le 100$ y $K \le 100$.
- Subtarea 4 (50 puntos): Sin restricciones adicionales.
