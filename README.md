
# Simulación de Coches Autónomos con Aprendizaje Evolutivo

Este proyecto es una simulación visual de coches autónomos controlados por redes neuronales simples, utilizando el motor gráfico `pygame`. Los coches aprenden a moverse en una pista evitando colisiones mediante un proceso evolutivo, seleccionando y cruzando las mejores redes neuronales generación tras generación.

---

## 🎮 Requisitos

- Python 3.7+
- pygame
- numpy

Instalación de dependencias:

```bash
pip install pygame numpy
```

## 📂 Estructura del proyecto

```
.
├── main.py                  # Ejecución principal de la simulación con una sola generación
├── evolution.py             # Ejecución principal con múltiples generaciones y evolución
├── playercar.py             # Lógica del coche y sensores
├── utils.py                 # Definición de red neuronal y funciones genéticas (mutación, cruce, etc.)
├── Images/
│   └── Sprites/
│       └── white_small.png  # Imagen del coche
├── bg7.png                  # Imagen de la pista
├── bg4.png                  # Imagen de colisión de la pista
├── README.md                # Este archivo
```

## 🤖 Funcionamiento

Cada coche cuenta con sensores virtuales que detectan distancias a obstáculos en varias direcciones.
Las entradas de estos sensores, junto con la velocidad actual, se pasan a una red neuronal simple que decide:

- Acelerar
- Frenar
- Girar a la derecha
- Girar a la izquierda

## 🚗 Lógica de Entrenamiento

- Se inicializan 200 coches con redes neuronales aleatorias.
- Cada red neuronal toma decisiones en función del entorno del coche.
- Cuando todos los coches colisionan o pasa cierto tiempo, se evalúan sus puntuaciones.
- Se seleccionan las mejores redes (TOP 10) y se cruzan entre sí, con mutaciones aleatorias, para crear la siguiente generación.

## ⏱ HUD en Pantalla

Durante la simulación se muestra:

- Tiempo transcurrido
- Autos vivos
- Generación actual (modo evolutivo)

## 🧠 Evolución Genética

El archivo `evolution.py` implementa la evolución de redes neuronales:

- `TOP_K = 10`: se seleccionan las 10 mejores redes.
- Se aplica crossover y mutación para generar nuevas redes hijas.
- Cada nueva generación trata de mejorar el rendimiento anterior.

## 💾 Guardado de Resultados

Se pueden guardar las mejores redes neuronales con la función `save_top_networks()`.

## 📷 Visual

La interfaz muestra:

- El coche en movimiento
- El fondo de la pista (`bg7.png`)
- Los sensores (opcional, desactivado por defecto)

## 📌 Uso

Para correr la simulación básica (una generación):

```bash
python main.py
```

Para correr la versión evolutiva (múltiples generaciones):

```bash
python evolution.py
```

## 🧩 Personalización

Puedes modificar:

- `NUM_CARS`: número de coches por generación
- `MUTATION_ROUNDS`: intensidad de mutación
- Arquitectura de la red neuronal (número de capas y neuronas)
- Imágenes de pista y colisión (`bg7.png`, `bg4.png`, etc.)

## 📄 Créditos

Proyecto de simulación educativa para experimentar con inteligencia artificial simple aplicada a conducción autónoma.
