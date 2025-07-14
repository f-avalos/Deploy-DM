from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np
# import pandas as pd
from sklearn.base import BaseEstimator
import os
import logging
from datetime import datetime

try:
    from config import Config
except ImportError:
    # Fallback configuration if config.py is not available
    class Config:
        FLASK_ENV = os.environ.get('FLASK_ENV', 'production')
        DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
        MODEL_PATH = os.environ.get('MODEL_PATH', 'best_model.pkl')
        PORT = int(os.environ.get('PORT', 5000))
        LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
        
        @staticmethod
        def is_production():
            return Config.FLASK_ENV == 'production'

# Configure logging
logging.basicConfig(level=getattr(logging, Config.LOG_LEVEL))
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration for production
app.config['ENV'] = Config.FLASK_ENV
app.config['DEBUG'] = Config.DEBUG

# Variable global para almacenar el modelo
model = None
model_loaded_at = None
prediction_count = 0

def load_model():
    """Carga el modelo PKL al iniciar la aplicación"""
    global model, model_loaded_at
    model_path = Config.MODEL_PATH
    
    if os.path.exists(model_path):
        try:
            with open(model_path, 'rb') as file:
                model = pickle.load(file)
            model_loaded_at = datetime.now()
            logger.info(f"Modelo cargado exitosamente desde {model_path}")
            logger.info(f"Tipo de modelo: {type(model).__name__}")
            return True
        except Exception as e:
            logger.error(f"Error al cargar el modelo: {e}")
            model = None
            return False
    else:
        logger.error(f"No se encontró el archivo del modelo en {model_path}")
        model = None
        return False

@app.route('/')
def home():
    """Ruta principal que renderiza la aplicación"""
    return render_template('app.html')

@app.route('/index')
def index():
    """Ruta alternativa que renderiza la aplicación"""
    return render_template('app.html')

@app.route('/api/data', methods=['GET'])
def get_data():
    """API endpoint para obtener información básica del sistema"""
    global model, model_loaded_at, prediction_count
    
    data = {
        "message": "Heart Attack Prediction API",
        "status": "success",
        "model_loaded": model is not None,
        "model_loaded_at": model_loaded_at.isoformat() if model_loaded_at else None,
        "prediction_count": prediction_count,
        "endpoints": {
            "predict": "/predict (POST)",
            "model_info": "/model-info (GET)",
            "health": "/health (GET)"
        }
    }
    return jsonify(data)

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de verificación de salud del servicio"""
    global model
    
    status = {
        "status": "healthy" if model is not None else "unhealthy",
        "model_loaded": model is not None,
        "environment": Config.FLASK_ENV,
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }
    
    status_code = 200 if model is not None else 503
    return jsonify(status), status_code

@app.route('/predict', methods=['POST'])
def predict():
    """Endpoint para realizar predicciones"""
    global model, prediction_count
    
    if model is None:
        logger.error("Intento de predicción con modelo no cargado")
        return jsonify({
            'error': 'Modelo no disponible. Verifique que el archivo best_model.pkl exista.',
            'status': 'error'
        }), 503
    
    try:
        # Obtener datos del formulario
        if request.is_json:
            data = request.get_json()
            logger.info("Datos recibidos (JSON)")
        else:
            data = request.form.to_dict()
            logger.info("Datos recibidos (Form)")
        
        logger.info(f"Datos de entrada: {data}")
        
        # Campos esperados del formulario
        form_features = [
            'PhysicalActivities', 'AlcoholDrinkers', 'ageCategoryGrouped', 
            'SmokerStatusGrouped', 'HadDiabetesGrouped', 'HadHeartAttack'
        ]
        
        # Validar que todos los campos estén presentes
        missing_fields = []
        form_data = {}
        
        for feature in form_features:
            if feature not in data or data[feature] == '':
                missing_fields.append(feature)
            else:
                try:
                    value = int(float(data[feature]))
                    # Validar rangos básicos
                    if feature == 'ageCategoryGrouped' and value not in [0, 1, 2]:
                        raise ValueError(f"debe ser 0, 1 o 2")
                    if feature == 'SmokerStatusGrouped' and value not in [0, 1, 2]:
                        raise ValueError(f"debe ser 0, 1 o 2")
                    if feature == 'HadDiabetesGrouped' and value not in [0, 1, 2]:
                        raise ValueError(f"debe ser 0, 1 o 2")
                    if feature in ['PhysicalActivities', 'AlcoholDrinkers', 'HadHeartAttack'] and value not in [0, 1]:
                        raise ValueError(f"debe ser 0 o 1")
                    
                    form_data[feature] = value
                except ValueError as e:
                    logger.error(f"Error de validación: {e}")
                    return jsonify({
                        'error': f'Valor inválido para {feature}: {str(e)}',
                        'status': 'error'
                    }), 400
        
        if missing_fields:
            logger.error(f"Campos faltantes: {missing_fields}")
            return jsonify({
                'error': f'Campos faltantes: {", ".join(missing_fields)}',
                'status': 'error'
            }), 400
        
        # Transformar datos del formulario a las features que espera el modelo
        # El modelo espera estas 7 features en este orden específico:
        model_features = [
            'PhysicalActivities_Yes',           # 1 si PhysicalActivities == 1, 0 si no
            'AlcoholDrinkers_Yes',              # 1 si AlcoholDrinkers == 1, 0 si no  
            'ageCategoryGrouped_Older adult',   # 1 si ageCategoryGrouped == 2, 0 si no
            'ageCategoryGrouped_Young',         # 1 si ageCategoryGrouped == 0, 0 si no
            'SmokerStatusGrouped_Former smoker', # 1 si SmokerStatusGrouped == 1, 0 si no
            'SmokerStatusGrouped_Never smoked', # 1 si SmokerStatusGrouped == 0, 0 si no
            'HadDiabetesGrouped_Yes'            # 1 si HadDiabetesGrouped == 1, 0 si no
        ]
        
        # Crear el array de entrada con las features transformadas
        input_data = [
            1 if form_data['PhysicalActivities'] == 1 else 0,          # PhysicalActivities_Yes
            1 if form_data['AlcoholDrinkers'] == 1 else 0,             # AlcoholDrinkers_Yes
            1 if form_data['ageCategoryGrouped'] == 2 else 0,          # ageCategoryGrouped_Older adult (65+)
            1 if form_data['ageCategoryGrouped'] == 0 else 0,          # ageCategoryGrouped_Young (18-44)
            1 if form_data['SmokerStatusGrouped'] == 1 else 0,         # SmokerStatusGrouped_Former smoker
            1 if form_data['SmokerStatusGrouped'] == 0 else 0,         # SmokerStatusGrouped_Never smoked
            1 if form_data['HadDiabetesGrouped'] == 1 else 0           # HadDiabetesGrouped_Yes
        ]
        
        # Convertir a numpy array y hacer predicción
        input_array = np.array(input_data).reshape(1, -1)
        logger.info(f"Datos del formulario: {form_data}")
        logger.info(f"Array transformado para el modelo: {input_array}")
        logger.info(f"Features del modelo: {model_features}")
        
        # Realizar predicción
        prediction = model.predict(input_array)[0]
        logger.info(f"Predicción: {prediction}")
        
        # Intentar obtener probabilidades si el modelo las soporta
        prob_no_attack = None
        prob_attack = None
        
        try:
            if hasattr(model, 'predict_proba'):
                probabilities = model.predict_proba(input_array)[0]
                prob_no_attack = float(probabilities[0])
                prob_attack = float(probabilities[1])
                logger.info(f"Probabilidades: No ataque={prob_no_attack:.3f}, Ataque={prob_attack:.3f}")
        except Exception as prob_error:
            logger.warning(f"No se pudieron obtener probabilidades: {prob_error}")
        
        # Incrementar contador de predicciones
        prediction_count += 1
        
        # Interpretar resultado
        result = {
            'prediction': int(prediction),
            'result': 'Alto riesgo de ataque al corazón' if prediction == 1 else 'Bajo riesgo de ataque al corazón',
            'probability_no_attack': prob_no_attack,
            'probability_attack': prob_attack,
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'input_features': form_data,
            'model_features': dict(zip(model_features, input_data))
        }
        
        logger.info(f"Resultado exitoso: predicción={prediction}")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error en predicción: {str(e)}")
        return jsonify({
            'error': f'Error interno del servidor: {str(e)}',
            'status': 'error',
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/model-info')
def model_info():
    """Endpoint para obtener información del modelo"""
    global model, model_loaded_at, prediction_count
    
    if model is None:
        return jsonify({
            'error': 'Modelo no disponible. Verifique que el archivo best_model.pkl exista.',
            'status': 'error'
        }), 503
    
    try:
        info = {
            'model_type': type(model).__name__,
            'model_module': type(model).__module__,
            'status': 'loaded',
            'loaded_at': model_loaded_at.isoformat() if model_loaded_at else None,
            'prediction_count': prediction_count,
            'environment': Config.FLASK_ENV,
            'debug_mode': Config.DEBUG,
            'form_features': [
                'PhysicalActivities', 'AlcoholDrinkers', 'ageCategoryGrouped', 
                'SmokerStatusGrouped', 'HadDiabetesGrouped', 'HadHeartAttack'
            ],
            'model_features': [
                'PhysicalActivities_Yes', 'AlcoholDrinkers_Yes',
                'ageCategoryGrouped_Older adult', 'ageCategoryGrouped_Young',
                'SmokerStatusGrouped_Former smoker', 'SmokerStatusGrouped_Never smoked',
                'HadDiabetesGrouped_Yes'
            ]
        }
        
        # Información adicional si está disponible
        if hasattr(model, 'feature_names_in_'):
            info['feature_names'] = model.feature_names_in_.tolist()
        
        if hasattr(model, 'n_features_in_'):
            info['n_features'] = model.n_features_in_
            
        if hasattr(model, 'classes_'):
            info['classes'] = model.classes_.tolist()
            
        if hasattr(model, 'feature_importances_'):
            info['has_feature_importances'] = True
        
        # Verificar si soporta probabilidades
        info['supports_probabilities'] = hasattr(model, 'predict_proba')
            
        return jsonify(info)
        
    except Exception as e:
        logger.error(f"Error al obtener información del modelo: {e}")
        return jsonify({
            'error': f'Error al obtener información del modelo: {str(e)}',
            'status': 'error'
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Manejador de errores 404"""
    return jsonify({
        'error': 'Endpoint no encontrado',
        'status': 'error'
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """Manejador de errores 405"""
    return jsonify({
        'error': 'Método no permitido',
        'status': 'error'
    }), 405

@app.errorhandler(500)
def internal_error(error):
    """Manejador de errores 500"""
    return jsonify({
        'error': 'Error interno del servidor',
        'status': 'error'
    }), 500

if __name__ == '__main__':
    # Cargar modelo al iniciar
    if load_model():
        logger.info("Aplicación iniciada correctamente")
        logger.info(f"Modo: {Config.FLASK_ENV}")
        # For production deployment
        if Config.is_production():
            app.run(host='0.0.0.0', port=Config.PORT)
        else:
            app.run(debug=Config.DEBUG, host='0.0.0.0', port=Config.PORT)
    else:
        logger.error("No se pudo cargar el modelo. Verificar archivo best_model.pkl")
        print("ERROR: No se pudo cargar el modelo. La aplicación no se iniciará.")
        print("Verificar que el archivo 'best_model.pkl' existe en el directorio actual.")