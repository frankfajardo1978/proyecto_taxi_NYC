![alt text](image-1.png)

¿Qué es Prophet?
Prophet es un modelo desarrollado por Facebook para el análisis de series temporales. Está diseñado para manejar:

- Tendencias lineales o no lineales.
- Estacionalidades (patrones que se repiten en el tiempo, com horarios, días de la semana o meses).
- Anomalías o eventos fuera de lo común.
- Series temporales con datos faltantes o irregulares.

Es ideal para datos con estacionalidades claras y tendencias a largo plazo.

¿Cómo funciona Prophet?
1. Descomposición de la serie temporal: Prophet descompone los datos en tres componentes principales:

    - Tendencia (Trend): Cambios a largo plazo (por ejemplo, aumento o disminución constante de la demanda).
    - Estacionalidad (Seasonality): Patrones repetitivos diarios, semanales, mensuales o anuales (como mayor demanda en ciertas horas del día).
    - Festividades o eventos (Holidays): Cambios en la demanda debido a eventos externos (opcional).
2. Modelo aditivo: La predicción se basa en la suma de estas componentes:

![alt text](image.png)

4. Ajustes automáticos: Prophet ajusta automáticamente los hiperparámetros (como periodicidades) basándose en los datos, por lo que es fácil de usar sin configuración avanzada.
