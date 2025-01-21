# Descripción del Proyecto
TaxiCom2.0 es una aplicación web interactiva desarrollada con FastAPI y Dash que permite analizar datos de demanda y ganancias de taxis en Nueva York, categorizados por taxis verdes y amarillos. La aplicación también ofrece herramientas avanzadas para predecir las mejores horas y rutas según datos históricos.

## Características Principales
1. Análisis de datos de demanda y ganancias:
  - Muestra gráficos interactivos sobre la cantidad de viajes y las ganancias promedio.
  - Permite filtrar los datos por día de la semana y tipo de taxi (verde o amarillo).
2. Análisis avanzado:
  - Genera mapas de calor para visualizar la demanda por horas y días.
  - Predice las mejores horas y rutas basadas en parámetros como distancia y ganancia promedio.
3. Interfaz web integrada:
  - FastAPI proporciona una estructura robusta para la API y la gestión de archivos estáticos.
  - Dash se encarga de los gráficos y la interactividad.
4. Procesamiento de datos en tiempo real:
  - Preprocesamiento y limpieza de datos para eliminar valores atípicos y rellenar valores faltantes.
  - Integración de modelos de predicción con Random Forest.

## Instalación
- Clonar el repositorio:
git clone https://github.com/usuario/taxicom2.0.git
cd taxicom2.0
- Instalar dependencias: Asegúrate de tener Python 3.8 o superior instalado. Luego, ejecuta:
pip install -r requirements.txt
- Estructura del directorio: Asegúrate de tener los siguientes archivos en el directorio:
  green_tripdata_2024-10_reducido.csv: Datos de taxis verdes.
  Yellow_Tripdata_2024-10_reducido.csv: Datos de taxis amarillos.
  transformed_taxi_zone_merged_with_locations.csv: Datos de zonas y ubicaciones.
Ejecutar la aplicación:

Copiar código
uvicorn main:app --reload
La aplicación estará disponible en el local o se puede deployar en Render

## Tecnologías Utilizadas
Backend: FastAPI
Frontend: Dash
Machine Learning: Random Forest (scikit-learn)
Gráficos: Plotly
Procesamiento de Datos: pandas, NumPy
Arquitectura Web: WSGI Middleware para integrar Dash con FastAPI
Contribuciones
Las contribuciones son bienvenidas. Por favor, abre un issue o envía un pull request con tus mejoras o correcciones.

Autor
Jerónimo Martínez
LinkedIn | GitHub

  Licencia
  Este proyecto está licenciado bajo la Licencia MIT.
