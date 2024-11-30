Descripción del Proyecto
Este proyecto es una aplicación web para la visualización en tiempo real de los datos generados por sensores. 
La aplicación permite a los usuarios consultar la información de los sensores a través de una API, visualizar los datos en una tabla organizada y realizar un gráfico interactivo para analizar los valores obtenidos. 
Además, los usuarios pueden aplicar filtros por ID del sensor y fecha, lo que facilita la consulta y el análisis de datos específicos.

Características Principales
Visualización de datos: Los datos del sensor se presentan en una tabla con las columnas de ID del sensor, fecha, hora y valor.
Gráfico interactivo: Los datos se muestran también en un gráfico de líneas que permite visualizar la evolución de los valores del sensor a lo largo del tiempo.
Filtros: Los usuarios pueden filtrar los datos según el ID del sensor y la fecha, lo que facilita la búsqueda de datos específicos.
Actualización dinámica: Los datos se actualizan dinámicamente sin necesidad de recargar la página, lo que mejora la experiencia de usuario.
Tecnologías Utilizadas
Frontend:

HTML5: Para la estructura básica de la página web.
Chart.js: Para la visualización de los datos en forma de gráfico interactivo.
Fetch API: Para hacer solicitudes a la API del backend y obtener los datos del sensor.
Backend:

Flask: Framework en Python para la creación de la API REST que maneja las solicitudes del frontend.
Firebase: Base de datos en tiempo real para almacenar y consultar los datos de los sensores.
Instalación
Clonar el repositorio:
Clona el repositorio del proyecto en tu máquina local utilizando Git.

git clone:
Instalar dependencias:
Navega a la carpeta del proyecto y crea un entorno virtual para instalar las dependencias necesarias.

cd tu-repositorio
python -m venv venv
source venv/bin/activate  # En Windows usa venv\Scripts\activate
pip install -r requirements.txt
Configurar Firebase:
Asegúrate de tener la clave del servicio de Firebase (firebase-adminsdk.json) en el directorio raíz del proyecto para poder conectarte a la base de datos de Firebase.

Ejecutar la aplicación:
Para iniciar el servidor de Flask, ejecuta el siguiente comando:

python app.py
La aplicación estará disponible en http://127.0.0.1:5000.