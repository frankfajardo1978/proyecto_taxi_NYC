# Readme appis. Machine Learning. 

Las siguientes apis han sido desarrolladas utilizando dos plataformas: render y streamlit. En ambas apis se desarrolla tanto la visualización como el desarrollo de modelos de Machine Learning con el fin de presentar analisis e insihgt robustos. A continuación se desarrollarán las apis.

### App de autos electricos en Streamlit. Analisis de la App para el negocio

Url app: https://taxicom2.streamlit.app/ 

1. Comparación de Marcas y Modelos
Funcionalidad:
Esta sección permite a los usuarios comparar marcas y modelos de vehículos eléctricos basándose en métricas clave como:
- Aceleración (accel): Indicador de la capacidad del vehículo para responder rápidamente.
- Velocidad máxima (topspeed): Útil para trayectos largos o zonas con autopistas.
- Autonomía (range): Mide cuánto puede viajar un vehículo con una sola carga, esencial para taxis que operan muchas horas al día.
- Eficiencia (efficiency): Kilómetros por kilovatio hora, indicador de costos operativos.
- Precio en USD (priceusd): Factor clave para evaluar el retorno de inversión (ROI).

Insight para el negocio:
- Optimización de flota: Ayuda a los propietarios de negocios de taxis a elegir vehículos que maximicen la autonomía y minimicen los costos operativos.
- Selección informada: Facilita decisiones sobre qué modelos son más rentables para operaciones prolongadas.
- Competitividad: Permite comparar directamente vehículos de fabricantes reconocidos como Tesla, BMW, o Polestar.

2. Recomendaciones

Funcionalidad:
- Mediante un algoritmo de clustering (DBSCAN), la app identifica vehículos similares en función de las variables seleccionadas. Esto permite al usuario encontrar alternativas a su modelo actual que se ajusten a necesidades específicas.

Insight para el negocio:
- Diversificación de opciones: Ofrece sugerencias sobre modelos similares que pueden ser más económicos o tener características específicas deseadas, como mayor eficiencia o menor costo inicial.
- Reducción del riesgo de decisión: Ayuda a los propietarios a explorar modelos confiables dentro de un mismo segmento.
Escalabilidad: Si un modelo resulta ser eficiente, se pueden identificar otros modelos en el mismo clúster para expandir la flota.

3. Predicción de Amortización

Funcionalidad:
Esta sección estima el tiempo necesario para que un taxi recupere su costo inicial (amortización), basándose en:
- Precio del vehículo.
- Ingresos diarios promedio calculados a partir de datos históricos.
- Ganancias netas ajustadas al porcentaje real que queda después de costos operativos.

Insight para el negocio:
- Planificación financiera: Ofrece a los propietarios un análisis claro sobre el tiempo de retorno de la inversión, crucial para evaluar riesgos y planificar expansiones.
- Toma de decisiones estratégicas: Identifica qué vehículos pueden generar un ROI más rápido y qué modelos podrían no ser adecuados para taxis.
- Optimización del flujo de caja: Permite priorizar compras de vehículos que garanticen un flujo de caja positivo más temprano.

4. Optimización de Rutas para Taxis

Funcionalidad:
Mediante el clustering de ubicaciones (utilizando KMeans), esta sección:
- Agrupa zonas de alta demanda según las ubicaciones de recogida (PULocationID) o destino (DOLocationID).
- Visualiza estos clusters en un mapa interactivo con folium.

Insight para el negocio:

- Estrategia basada en demanda: Permite identificar áreas con mayor densidad de pasajeros, ayudando a los conductores a posicionarse estratégicamente.
- Reducción de tiempos muertos: Minimiza los tiempos en los que los taxis circulan vacíos, aumentando la rentabilidad.
- Segmentación geográfica: Ayuda a entender patrones de demanda en diferentes horarios o días de la semana, optimizando recursos humanos y vehiculares.
- Planificación de expansión: Si un área tiene una alta concentración de recogidas o destinos, esto puede indicar la necesidad de aumentar la flota en esa región.

#### Conclusión General

Esta aplicación ofrece herramientas prácticas y basadas en datos para el negocio de taxis eléctricos. Sus funcionalidades están diseñadas para resolver problemas clave como:
- Optimización de la flota (comparación de modelos).
- Toma de decisiones informadas (recomendaciones).
- Gestión financiera estratégica (predicción de amortización).
- Eficiencia operativa y logística (optimización de rutas).

Impacto Potencial:

- Reducción de costos: Al elegir vehículos eficientes y operarlos estratégicamente.
- Aumento de ingresos: Al maximizar el tiempo productivo y aprovechar zonas de alta demanda.
- Decisiones basadas en datos: Minimiza la incertidumbre y aumenta la confiabilidad en cada inversión o estrategia operativa.

### App de demanda y predicción de zonas para taxis amarillos. Render. 

Url App: https://ml-taxisny.onrender.com/ 

1. Objetivo de la App: La aplicación combina análisis de datos con funcionalidades de predicción y visualización, específicamente enfocada en datos de viajes de taxis (taxis verdes y amarillos en Nueva York). Ofrece insights sobre patrones de demanda, ingresos promedio y rutas óptimas, utilizando herramientas como FastAPI para el backend, Dash para la visualización interactiva, y modelos de machine learning para predicciones.

2. Principales Funcionalidades
- Carga y Preprocesamiento de Datos:
	+ Los datos de viajes de taxis verdes y amarillos son procesados para incluir características clave como:
		+ Hora y día del viaje.
		+ Ubicación de recogida.
		+ Ingreso y distancia promedio del viaje.
	+ Se eliminan valores atípicos para garantizar análisis más precisos.
- Análisis de Demanda Semanal:
	+ Agrega y presenta información sobre la cantidad de viajes, ingresos promedio, y horas pico en diferentes zonas y días de la semana.
	+ Permite a los usuarios identificar zonas y horarios con alta demanda.
- Visualización Interactiva (Dash):
	+ Gráficos para Taxis Verdes y Amarillos:
		+ Comparación de la cantidad de viajes y ganancias promedio por zona.
	+ Heatmap:
		+ Muestra patrones de demanda por horas y días en zonas específicas.
		+ Predicciones de Horarios y Rutas Óptimas:
- Utiliza un modelo de Random Forest para predecir:
	+ La mejor hora para operar en una zona específica.
	+ El recorrido promedio.
	+ La ganancia estimada.
- Integración en un Ecosistema Web:
	+ Ofrece una interfaz de usuario moderna y visual mediante Dash, montada sobre FastAPI, accesible a través de un navegador.

3. Utilidad para el Negocio de Taxis
- Optimización de Operaciones: Identificar zonas y horarios de alta demanda permite a los conductores y empresas asignar recursos eficientemente, maximizando ingresos y reduciendo tiempos muertos.
- Mejora en la Planificación: Los datos históricos procesados ayudan a tomar decisiones basadas en patrones reales de demanda, especialmente útiles en eventos especiales o temporadas.
- Predicciones y Recomendaciones: Al predecir horarios óptimos y rutas más rentables, los conductores pueden optimizar sus recorridos, reduciendo costos operativos y aumentando su rentabilidad.
- Estrategias de Expansión: La información sobre la distribución de la demanda en diferentes zonas y días permite a las empresas planificar estrategias de expansión o promoción en áreas menos explotadas.
- Interfaz Amigable: La visualización interactiva simplifica la comprensión de datos complejos, haciendo accesible la información a usuarios con poca experiencia técnica.

4. Conclusión
Esta aplicación ofrece un enfoque integral para la gestión y optimización del negocio de taxis, combinando análisis de datos, machine learning, y visualización interactiva. Proporciona herramientas clave para mejorar la rentabilidad y eficiencia operativa, y su arquitectura modular permite escalarla o personalizarla según las necesidades de diferentes mercados.
