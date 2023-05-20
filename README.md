# CC5513-T2-Deteccion_de_Planos
Código desarrollado como parte de una tarea del ramo CC5513, Procesamiento geométrico y análisis de formas, dictado por el profesor Iván Sipirán en la Universidad de Chile

### Ejecución del Código
El programa principal `main.py` se ejecuta desde la línea de comandos. Se le pueden suplir los siguientes argumentos:
 - `--file`: nombre del archivo con la nube de puntos. Debe ser de formato `.xyz` o de aquellos soportados por openmesh. Defecto: "cube.xyz"
 - `--threshold`: define la distancia máxima a la cual un punto se considera como parte de un plano.
 - `--inliers`: número mínimo de puntos dentro de un plano para que éste se considere como válido
 - `--cmap`: cambia el mapa de colores usado en la visualización de polyscope.

### Resultados Empíricos
 - `cube.xyz`: detecta sin problemas los 6 planos con threshold de 0.01 e inliers de 500
 - `icosahedron.xyz`: nube de 10k puntos generada artifialmente en el script `gen_icosahedron.py`. Se logra detectar la mayoría de las 20 caras sin problemas con threshold de 0.004 e inliers de 400
 - 