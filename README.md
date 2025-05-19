https://github.com/Malenizeta/machine_arcade.git

# Máquina Arcade Distribuida en Python 

## Descripción General

Este proyecto consiste en el desarrollo de una **Máquina Arcade distribuida** implementada en Python. La arquitectura se basa en el modelo **cliente-servidor**, donde tres juegos clásicos de lógica actúan como clientes independientes que se comunican con un **servidor central**. Dicho servidor es responsable de almacenar los resultados de las partidas en una base de datos SQLite mediante SQLAlchemy.

Cada juego incorpora una **interfaz gráfica**, ambientada en el mundo de Mario Bros. 

---
## Nuevas funcionalidades añadidas (segunda parte práctica)

**1. Chatbot interactivo desde el menú principal:**

Se ha incorporado un chatbot accesible directamente desde el menú principal, que permite realizar consultas interactivas sobre fórmulas, estrategias y dudas relacionadas con los juegos. Este chatbot enriquece la dimensión educativa de la aplicación y ofrece soporte en tiempo real al usuario.

![Captura de pantalla 2025-05-19 183804](https://github.com/user-attachments/assets/4c3b7f9c-8184-44a2-b140-3ff6d0388b11)
![Captura de pantalla 2025-05-19 193651](https://github.com/user-attachments/assets/bba6fb45-30b6-49e1-888b-6afdc1fec2f9)

**2. Sistema de ayuda basado en IA en cada juego:**

En cada juego se ha añadido un botón “Ayuda IA” que permite enviar el estado actual del juego a un servicio externo de inteligencia artificial. Este servicio devuelve recomendaciones y sugerencias estratégicas para ayudar al jugador durante la partida.
![Captura de pantalla 2025-05-20 010814](https://github.com/user-attachments/assets/d9e5864d-5e67-4d27-8d02-699f38fc02b9)
![Captura de pantalla 2025-05-20 005138](https://github.com/user-attachments/assets/ad84fb9b-e29a-428f-afbf-675677e186e9)
![Captura de pantalla 2025-05-20 002519](https://github.com/user-attachments/assets/3076bc14-4e5c-49b0-9d2e-24c313b852b1)

Nota: Debido al límite de consultas gratuitas al servicio de IA, actualmente no se dispone de imágenes que muestren las respuestas devueltas en tiempo real. Sin embargo, se han realizado pruebas exhaustivas previas que confirman el correcto funcionamiento del sistema. Por ejemplo, en el caso del chatbot, existe una captura de pantalla con una respuesta típica, aunque la interfaz aún estaba en desarrollo.
![Captura de pantalla 2025-05-19 184738](https://github.com/user-attachments/assets/c3b318f5-f8a9-45d2-91b6-df5128ebe165)

---

## Juegos Incluidos

### 1. N Reinas
El usuario debe colocar N reinas en un tablero N×N sin que se ataquen entre sí. El juego permite:
- Seleccionar el valor de N.
- Interfaz para colocar reinas.
- Posibilidad de mover las fichas una vez colocadas.
- Enviar resultados al servidor tras completar o abandonar la partida.

**Datos registrados en servidor:**
- Tamaño del tablero (N).
- Resultado (resuelto o no).
- Número de movimientos.

![Captura de pantalla 2025-05-08 225244](https://github.com/user-attachments/assets/27da0ec8-1f69-416b-b786-5046a94c941e)

---

### 2. Recorrido del Caballo
El jugador controla un caballo que debe recorrer un tablero (por defecto 8x8), visitando todas las casillas exactamente una vez:
- Se puede elegir la posición inicial.
- Se registra el recorrido final.

**Datos registrados en servidor:**
- Tamaño del tablero (N).
- Resultado (resuelto o no).
- Número de movimientos.

![Captura de pantalla 2025-05-08 220527](https://github.com/user-attachments/assets/2a75d730-3b10-4aba-8977-749651f747f1)
![Captura de pantalla 2025-05-08 220852](https://github.com/user-attachments/assets/9a87d922-82cd-40c3-b2cf-f7d3aeb607ec)

---

### 3. Torres de Hanói
Se presentan tres postes y un número de discos. El jugador debe mover todos los discos al poste destino cumpliendo las reglas del puzzle:
- El usuario elige cuántos discos utilizar.
- Movimientos válidos mediante GUI.
- Comparación opcional con el número mínimo teórico.

**Datos registrados en servidor:**
- Número de discos.
- Número de movimientos realizados.
- Número de movimientos mínimos.
- Si el usuario ha completado el juego en el número mínimo de movimientos.
  
![Captura de pantalla 2025-05-08 225651](https://github.com/user-attachments/assets/45b1ca15-2f7e-467f-a668-5d316ccbb051)

---

## Organización del Proyecto

El sistema sigue una arquitectura **cliente-servidor**:

- Cada juego actúa como **cliente** y se comunica con un servidor Python vía **sockets TCP/IP**.
- El servidor utiliza **hilos (threads)** para aceptar múltiples conexiones concurrentes.
- Los resultados de las partidas se guardan en una base de datos **SQLite** (`results.db`) mediante **SQLAlchemy**.

![Captura de pantalla 2025-05-08 230535](https://github.com/user-attachments/assets/c246c0b5-7cf9-499f-904d-e7ff7cb39881)

---

## Estructura del Proyecto

```plaintext
MACHINE_ARCADE/
├── __pycache__/
├── assets/
│   ├── fonts/
│   └── images/
├── games/
│   ├── __pycache__/
│   ├── __init__.py
│   ├── caballo_tour.py
│   ├── n_reinas.py
│   └── torres_hanoi.py
├── gui/
│   ├── __pycache__/
│   ├── __init__.py
│   ├── caballo_gui.py
│   ├── menu.py
│   ├── n_reinas_gui.py
│   └── torres_hanoi_gui.py
├── server/
│   ├── __pycache__/
│   ├── __init__.py
│   └── server.py
├── client.py
├── ia_client.py
├── main.py
├── README.md
├── requirements.txt
└── results.db
```
---

## Instalación y Ejecución

Sigue los pasos a continuación para poner en marcha el sistema:

1. **Clonar el repositorio**

2. **Ejecutar el servidor (necesario para guardar resultados)**:
  cd server
  python server.py

3. **Ejecutar un juego (desde la raíz del proyecto)**:
  python main.py
