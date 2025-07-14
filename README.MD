# Heart Attack Prediction - Deploy DM

## 📋 Descripción

Aplicación web de predicción de ataques al corazón utilizando Machine Learning. La aplicación utiliza Flask como backend y una interfaz web moderna y responsiva para interactuar con el modelo de predicción.

## 🚀 Características Principales

### ✨ Interfaz Web Mejorada
- **Diseño moderno y responsivo** con Bootstrap 5
- **Interfaz unificada** - Combinación de templates en un solo archivo
- **Experiencia de usuario mejorada** con animaciones y feedback visual
- **Validación en tiempo real** de formularios
- **Indicadores de carga** y estados de la aplicación
- **Diseño gradient** con efectos visuales atractivos
- **Iconos Font Awesome** para mejor UX

### 🔧 Backend Robusto
- **Logging completo** para monitoreo y debugging
- **Validación de datos exhaustiva** con mensajes de error específicos
- **Manejo de errores mejorado** con códigos de estado HTTP apropiados
- **API REST bien estructurada** con múltiples endpoints
- **Health checks** para monitoreo del sistema
- **Contador de predicciones** y estadísticas
- **Información detallada del modelo** cargado

### 📊 Funcionalidades de Predicción
- **6 características de entrada**:
  - Actividades Físicas
  - Consumo de Alcohol
  - Categoría de Edad (18-44, 45-64, 65+)
  - Estado de Fumador
  - Estado de Diabetes
  - Historial de Ataques Previos
- **Predicción binaria** (Alto/Bajo riesgo)
- **Probabilidades** cuando el modelo las soporta
- **Recomendaciones personalizadas** según el resultado

## 🛠️ Instalación y Configuración

### Requisitos Previos
- Python 3.8+
- pip

### Pasos de Instalación

1. **Clonar/Descargar el proyecto**
   ```bash
   cd Deploy-DM
   ```

2. **Crear entorno virtual (recomendado)**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno (opcional para desarrollo local)**
   ```bash
   # Copiar el archivo de ejemplo
   cp .env.example .env
   
   # Editar .env según necesidades
   ```

5. **Verificar modelo**
   - Asegúrese de que `best_model.pkl` esté en el directorio raíz
   - El modelo debe ser compatible con scikit-learn

6. **Ejecutar la aplicación**
   ```bash
   python main.py
   ```

7. **Acceder a la aplicación**
   - Abrir navegador web en: `http://127.0.0.1:5000`

## 🚀 Despliegue en Render

### Preparación para Despliegue

El proyecto incluye todos los archivos necesarios para el despliegue en Render:

- `Procfile` - Comando de inicio para Render
- `runtime.txt` - Versión de Python
- `requirements.txt` - Dependencias (incluye gunicorn)
- `RENDER_DEPLOYMENT.md` - Guía detallada de despliegue

### Variables de Entorno para Render

Configure las siguientes variables de entorno en su dashboard de Render:

| Variable | Valor | Descripción |
|----------|-------|-------------|
| `FLASK_ENV` | `production` | Modo de Flask |
| `FLASK_DEBUG` | `false` | Desactiva debug en producción |
| `MODEL_PATH` | `best_model.pkl` | Ruta del modelo ML |

### Pasos de Despliegue

1. **Subir código a GitHub/GitLab**
2. **Conectar repositorio a Render**
3. **Configurar variables de entorno**
4. **Establecer comandos de construcción e inicio**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn main:app --host=0.0.0.0 --port=$PORT`

Para más detalles, consulte `RENDER_DEPLOYMENT.md`.

## 📡 API Endpoints

### 🏠 Frontend
- `GET /` - Página principal de la aplicación
- `GET /index` - Alias para la página principal

### 🔍 Información del Sistema
- `GET /api/data` - Información general del sistema
- `GET /health` - Estado de salud del servicio
- `GET /model-info` - Información detallada del modelo ML

### 🤖 Predicción
- `POST /predict` - Realizar predicción

#### Ejemplo de uso del endpoint de predicción:

```javascript
// Datos de entrada
{
  "PhysicalActivities": "1",      // 0=No, 1=Sí
  "AlcoholDrinkers": "0",         // 0=No, 1=Sí
  "ageCategoryGrouped": "1",      // 0=18-44, 1=45-64, 2=65+
  "SmokerStatusGrouped": "0",     // 0=Nunca, 1=Ex-fumador, 2=Actual
  "HadDiabetesGrouped": "0",      // 0=No, 1=Sí, 2=Prediabetes
  "HadHeartAttack": "0"           // 0=No, 1=Sí
}

// Respuesta exitosa
{
  "prediction": 0,
  "result": "Bajo riesgo de ataque al corazón",
  "probability_no_attack": 0.85,
  "probability_attack": 0.15,
  "status": "success",
  "timestamp": "2025-01-14T10:30:00",
  "input_features": { ... }
}
```

## 🧪 Testing

### Test Automático
Ejecutar el script de pruebas:
```bash
# Con el servidor corriendo en otra terminal
python test_app.py
```

### Test Manual
1. Completar el formulario en la interfaz web
2. Verificar que todos los campos sean obligatorios
3. Probar con diferentes combinaciones de valores
4. Verificar que las probabilidades se muestren correctamente

## 📁 Estructura del Proyecto

```
Deploy-DM/
├── main.py                    # Aplicación Flask principal
├── best_model.pkl            # Modelo de ML entrenado
├── test_app.py               # Script de pruebas
├── requirements.txt          # Dependencias Python (actualizado)
├── Procfile                  # Comando de inicio para Render
├── runtime.txt               # Versión de Python para Render
├── .env.example              # Variables de entorno de ejemplo
├── .gitignore                # Archivos a ignorar en Git
├── README.md                 # Documentación
├── RENDER_DEPLOYMENT.md      # Guía de despliegue
├── templates/
│   └── app.html             # Template unificado (HTML + CSS + JS)
└── __pycache__/             # Cache de Python
```

## 🔧 Mejoras Implementadas

### 🎨 Frontend
- **Unificación de templates**: `index.html` y `content.html` combinados en `app.html`
- **Diseño responsivo**: Compatible con dispositivos móviles
- **UI moderna**: Gradientes, animaciones, iconos
- **Validación mejorada**: Feedback visual en tiempo real
- **Loading states**: Indicadores de carga durante las peticiones
- **Modal de información**: Detalles del modelo cargado

### ⚙️ Backend
- **Logging estructurado**: Mensajes informativos y de error
- **Validación robusta**: Verificación de tipos y rangos de datos
- **Error handling**: Manejo apropiado de excepciones
- **Health monitoring**: Endpoints para verificar estado del sistema
- **API documentation**: Respuestas JSON bien estructuradas
- **Performance tracking**: Contador de predicciones realizadas

### 🔒 Seguridad y Robustez
- **Validación de entrada**: Verificación de todos los parámetros
- **Error messages**: Mensajes de error informativos sin exponer detalles internos
- **Status codes**: Códigos HTTP apropiados para cada situación
- **Input sanitization**: Limpieza y validación de datos de entrada

## 🚨 Troubleshooting

### Problemas Comunes

1. **Error al cargar el modelo**
   ```
   ERROR: No se pudo cargar el modelo
   ```
   - Verificar que `best_model.pkl` existe
   - Verificar compatibilidad de versiones de scikit-learn

2. **Error de conexión en el frontend**
   ```
   Error de conexión: Failed to fetch
   ```
   - Verificar que Flask esté ejecutándose
   - Verificar que no haya conflictos de puerto

3. **Advertencia de versión de scikit-learn**
   ```
   InconsistentVersionWarning
   ```
   - Es una advertencia, no afecta la funcionalidad
   - Para eliminarla, entrenar el modelo con la versión actual

### Logs de Debug
Los logs se muestran en la consola donde se ejecuta `main.py`. Niveles de log:
- `INFO`: Operaciones normales
- `ERROR`: Errores que requieren atención
- `WARNING`: Situaciones que pueden requerir revisión

## 📈 Próximas Mejoras

- [ ] Autenticación de usuarios
- [ ] Historial de predicciones
- [ ] Exportar resultados a PDF
- [ ] Dashboard de estadísticas
- [ ] API rate limiting
- [ ] Containerización con Docker
- [ ] Tests unitarios automatizados

## 📝 Licencia

Este proyecto es de uso educativo y de demostración.

## 👥 Contribución

Para contribuir al proyecto:
1. Fork el repositorio
2. Crear una rama para la nueva funcionalidad
3. Realizar los cambios
4. Ejecutar las pruebas
5. Crear un Pull Request

---

**Desarrollado con ❤️ para Deploy DM**