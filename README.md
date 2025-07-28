# tipo_cambio_service

## Descripción General
Este proyecto es un servicio de consulta y conversión de tipo de cambio oficial del Banco Central de Costa Rica (BCCR). Permite obtener el tipo de cambio de compra y venta para una fecha específica y convertir montos de colones a dólares. Está construido en Python, utiliza FastAPI y puede ejecutarse en un contenedor Docker.

## Estructura del Proyecto
```
tipo_cambio_service/
├── Dockerfile
├── main.py
├── tipo_cambio.py
├── db.py
├── requirements.txt
├── .env
└── README.md
```

## Descripción de Archivos
- **Dockerfile**: Instrucciones para construir la imagen Docker de la aplicación.
- **main.py**: Punto de entrada de la aplicación, define los endpoints de la API.
- **tipo_cambio.py**: Lógica para consultar el tipo de cambio oficial desde el webservice SOAP del BCCR.
- **db.py**: Manejo de la base de datos SQLite y definición de modelos.
- **requirements.txt**: Lista de dependencias de Python necesarias para el proyecto.
- **.env**: Variables de entorno como credenciales, tokens y configuración de la base de datos.

## Instrucciones de Instalación
1. Clona el repositorio:
   ```
   git clone <repository-url>
   cd tipo_cambio_service
   ```

2. Crea y activa un entorno virtual:
   ```
   python -m venv venv
   # En Linux/Mac:
   source venv/bin/activate
   # En Windows:
   venv\Scripts\activate
   ```

3. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```

4. Configura tus variables de entorno en el archivo `.env`.

5. Ejecuta la aplicación localmente:
   ```
   uvicorn main:app --reload
   ```

6. O ejecuta en Docker:
   ```
   docker build -t tipo-cambio-service .
   docker run -p 8000:8000 --env-file .env tipo-cambio-service
   ```

## Uso
Una vez en ejecución, puedes acceder a la documentación interactiva en [http://localhost:8000/docs](http://localhost:8000/docs).

### Endpoints principales:
- **POST `/convertir/`**  
  Convierte un monto en colones a dólares usando el tipo de cambio de compra o venta para una fecha específica.
  ```json
  {
    "monto_colones": 100000,
    "fecha": "2025-07-26",
    "tipo": "venta"
  }
  ```
  Requiere el header: `X-API-KEY`.

- **GET `/tipo_cambio/?fecha=YYYY-MM-DD`**  
  Devuelve el tipo de cambio de compra y venta para la fecha indicada.
  ```json
  {
    "fecha": "2025-07-26",
    "venta": 506,
    "compra": 496
  }
  ```

## Obtención del Token del BCCR
Para consumir el webservice del BCCR necesitas un token de acceso.  
Puedes inscribirte y obtener tu token en el siguiente enlace oficial:  
[https://www.bccr.fi.cr/indicadores-economicos/servicio-web](https://www.bccr.fi.cr/indicadores-economicos/servicio-web)

Consulta también la [documentación técnica oficial (PDF)](https://gee.bccr.fi.cr/indicadoreseconomicos/Documentos/DocumentosMetodologiasNotasTecnicas/Webservices_de_indicadores_economicos.pdf) para más detalles sobre el uso del servicio.

## Contribuciones
¡Las contribuciones son bienvenidas! Por favor, abre un issue o envía un pull request para mejoras o correcciones.

## Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE