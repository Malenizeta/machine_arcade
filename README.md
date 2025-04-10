# Máquina Arcade Distribuida con IA

Este proyecto es una implementación de una Máquina Arcade Distribuida en Python. La aplicación integra tres puzzles clásicos:

- **N Reinas**
- **Recorrido del Caballo**
- **Torres de Hanói**

Utiliza una arquitectura cliente-servidor y emplea hilos (threads) para gestionar la comunicación asíncrona. La persistencia se realiza mediante SQLAlchemy y una base de datos SQLite. Además, se incorpora una herramienta de Inteligencia Artificial (IA) basada en el modelo **microsoft/DialoGPT-medium** de Hugging Face. La integración con la IA permite:

- **Ayuda IA:** Un botón en cada juego que, al pulsarse, envía el estado actual del juego a la API de Hugging Face para obtener sugerencias o estrategias.
- **Chatbot Interactivo:** Un módulo (o panel) que permite realizar consultas en lenguaje natural sobre fórmulas matemáticas y conceptos teóricos relacionados con los puzzles.

---

## Requisitos del Proyecto

- **Python 3.6+**
- **Dependencias:**
  - [SQLAlchemy==1.4.46](https://www.sqlalchemy.org/)
  - [requests==2.28.1](https://docs.python-requests.org/)
- **Base de Datos:** SQLite (se crea automáticamente en `results.db`).
- **Modelo de IA:** microsoft/DialoGPT-medium de Hugging Face (se accede mediante la API de Inference).

---

## Estructura del Proyecto

```plaintext
machine_arcade/
├── main.py
├── requirements.txt
├── games/
│   ├── __init__.py
│   ├── n_reinas.py
│   ├── caballo_tour.py
│   └── torres_hanoi.py
├── gui/
│   ├── __init__.py
│   ├── menu.py
│   ├── n_reinas_gui.py
│   ├── caballo_gui.py
│   └── torres_hanoi_gui.py
├── ia_client.py
└── server/
    ├── __init__.py
    └── server.py

```
### Descripción de Archivos
- **main.py:** Punto de entrada del programa. Inicializa la GUI y el servidor.
- **requirements.txt:** Lista de dependencias del proyecto.
- **games/:** Contiene la lógica de los juegos implementados.
  - **n_reinas.py:** Implementación del juego N Reinas.
  - **caballo_tour.py:** Implementación del recorrido del caballo.
  - **torres_hanoi.py:** Implementación de las Torres de Hanói.
- **gui/:** Contiene la interfaz gráfica de usuario para cada juego.
    - **menu.py:** Menú principal de la máquina arcade.
    - **n_reinas_gui.py:** Interfaz gráfica para el juego N Reinas.
    - **caballo_gui.py:** Interfaz gráfica para el recorrido del caballo.
    - **torres_hanoi_gui.py:** Interfaz gráfica para las Torres de Hanói.
- **ia_client.py:** Cliente para interactuar con la API de IA de Hugging Face.
- **server/:** Contiene la implementación del servidor.
  - **server.py:** Implementación del servidor que gestiona las conexiones y la lógica de los juegos.
---
## Instalación y Configuración

### Instalación

Para instalar el proyecto, clona el repositorio en tu máquina local:

1. **Clonar el Repositorio**  
   Ejecuta los siguientes comandos en tu terminal:

   ```bash
   git clone <URL-del-repositorio>
   cd machine_arcade


## Ejecución del Proyecto
Para ejecutar el proyecto, asegúrate de tener instaladas todas las dependencias. Puedes instalar las dependencias utilizando el siguiente comando:

```bash
pip install -r requirements.txt
```
Luego, puedes iniciar el servidor y la interfaz gráfica de usuario (GUI) ejecutando:

```bash
python main.py
```
Esto abrirá la ventana principal de la máquina arcade, donde podrás seleccionar el juego que deseas jugar. La IA estará disponible para ayudarte en cada juego y también podrás interactuar con el chatbot para resolver dudas o aprender más sobre los puzzles.

### 3. Configurar la API Key de Hugging Face

Para conectar la aplicación con el modelo de IA de Hugging Face, sigue estos pasos:

1. **Crea una Cuenta o Inicia Sesión**  
   - Visita [huggingface.co](https://huggingface.co) y regístrate o inicia sesión.

2. **Genera tu API Key**  
   - Haz clic en tu avatar (generalmente en la esquina superior derecha) y selecciona "Settings".  
   - En el menú lateral, selecciona "Access Tokens".  
   - Haz clic en "New token" o "Generate new token".  
   - Especifica un nombre para el token (por ejemplo, "MachineArcadeToken") y elige el nivel de permisos (la opción por defecto suele ser suficiente).  
   - Haz clic en "Generate" y copia la API Key generada.

3. **Configura el Token en el Proyecto**  
   - Abre el archivo `ia_client.py` y reemplaza la cadena `"TU_API_KEY_AQUI"` por la API Key que has copiado.

   **Ejemplo:**

   ```python
   API_KEY = "TU_API_KEY_GENERADA"  # Reemplaza con tu API Key de Hugging Face

  ## Ejecución del Proyecto

### Iniciar el Servidor

El servidor se ejecuta en segundo plano para atender las peticiones de clientes. Se lanza automáticamente al ejecutar el proyecto desde `main.py`.

```bash
python [main.py](http://_vscodecontentref_/0)

```
### Iniciar la Interfaz Gráfica
La interfaz gráfica se inicia automáticamente al ejecutar el proyecto desde `main.py`. Desde allí, puedes seleccionar el juego que deseas jugar y acceder a la ayuda de IA.
```bash
python main.py
```
### Interacción con la IA

La IA está integrada en cada juego. Al pulsar el botón de ayuda, se enviará el estado actual del juego a la API de Hugging Face y recibirás sugerencias o estrategias para avanzar en el juego.
### Chatbot Interactivo
El chatbot interactivo está disponible en la interfaz gráfica. Puedes hacer preguntas en lenguaje natural sobre fórmulas matemáticas y conceptos teóricos relacionados con los puzzles. La IA responderá basándose en el modelo de Hugging Face.
### Ejemplo de Pregunta
Puedes preguntar cosas como:
- "¿Cuál es la fórmula para calcular el número de movimientos en Torres de Hanói?"
- "¿Cómo puedo resolver el puzzle de N Reinas?"
- "¿Cuáles son las estrategias para el recorrido del caballo?"
```
### Ejemplo de Respuesta
La IA responderá con información relevante y sugerencias basadas en el estado actual del juego y tus preguntas.
```bash
{
  "response": "Para resolver el puzzle de N Reinas, puedes utilizar un enfoque de backtracking. Comienza colocando una reina en la primera fila y avanza fila por fila, asegurándote de que no haya conflictos con las reinas ya colocadas."
}
```
### Ejemplo de Respuesta
La IA responderá con información relevante y sugerencias basadas en el estado actual del juego y tus preguntas.
```bash
{
  "response": "Para resolver el puzzle de N Reinas, puedes utilizar un enfoque de backtracking. Comienza colocando una reina en la primera fila y avanza fila por fila, asegurándote de que no haya conflictos con las reinas ya colocadas."
}
```
### Uso de la Interfaz Gráfica
La interfaz gráfica es intuitiva y fácil de usar. Desde el menú principal, puedes seleccionar el juego que deseas jugar. Cada juego tiene su propia interfaz con botones para interactuar, reiniciar el juego y solicitar ayuda de IA.
### Ejemplo de Interfaz Gráfica

Al ejecutar python main.py, se despliega el menú principal.

Selecciona uno de los juegos (N Reinas, Recorrido del Caballo o Torres de Hanói) en la ventana emergente.
Dentro de cada juego podrás:
Iniciar el juego (por ejemplo, generar la solución de N Reinas).
Usar el botón "Ayuda IA" para obtener sugerencias basadas en el estado actual del juego.
Visualizar la solución o los movimientos recomendados en un cuadro de texto.

### Notas Adicionales
- Asegúrate de tener conexión a Internet para acceder a la API de Hugging Face.
- La base de datos SQLite se crea automáticamente al iniciar el servidor. Puedes encontrarla en el directorio raíz del proyecto como `results.db`.
- La aplicación está diseñada para ser extensible. Puedes agregar más juegos o funcionalidades siguiendo la estructura existente.

## Contribuciones
Las contribuciones son bienvenidas. Si deseas colaborar en el proyecto, por favor sigue estos pasos