#!/usr/bin/env python3
"""
Test script para verificar la funcionalidad de la aplicación Flask
de predicción de ataques al corazón.
"""

import requests
import json
import time

# Configuración
BASE_URL = "http://127.0.0.1:5000"

def test_endpoint(url, method="GET", data=None, expected_status=200):
    """Función para probar endpoints"""
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data, headers={'Content-Type': 'application/json'})
        
        print(f"\n{method} {url}")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == expected_status:
            print("✅ SUCCESS")
        else:
            print(f"❌ FAILED - Expected {expected_status}")
        
        # Mostrar respuesta JSON si es posible
        try:
            response_json = response.json()
            print(f"Response: {json.dumps(response_json, indent=2)}")
        except:
            print(f"Response text: {response.text}")
            
        return response
        
    except requests.exceptions.ConnectionError:
        print(f"❌ ERROR - No se pudo conectar a {url}")
        print("Asegúrese de que el servidor Flask esté ejecutándose")
        return None
    except Exception as e:
        print(f"❌ ERROR - {str(e)}")
        return None

def run_tests():
    """Ejecutar todas las pruebas"""
    print("🧪 Iniciando pruebas de la aplicación...")
    print("=" * 50)
    
    # Test 1: Verificar que el servidor esté corriendo
    print("\n1. Verificando servidor...")
    response = test_endpoint(f"{BASE_URL}/")
    if response is None or response.status_code != 200:
        print("❌ El servidor no está respondiendo. Verifique que main.py esté ejecutándose.")
        return
    
    # Test 2: API data endpoint
    print("\n2. Probando endpoint /api/data")
    test_endpoint(f"{BASE_URL}/api/data")
    
    # Test 3: Health check
    print("\n3. Probando endpoint /health")
    test_endpoint(f"{BASE_URL}/health")
    
    # Test 4: Model info
    print("\n4. Probando endpoint /model-info")
    test_endpoint(f"{BASE_URL}/model-info")
    
    # Test 5: Predicción válida
    print("\n5. Probando predicción válida")
    valid_data = {
        "PhysicalActivities": "1",
        "AlcoholDrinkers": "0",
        "ageCategoryGrouped": "1",
        "SmokerStatusGrouped": "0",
        "HadDiabetesGrouped": "0",
        "HadHeartAttack": "0"
    }
    test_endpoint(f"{BASE_URL}/predict", method="POST", data=valid_data)
    
    # Test 6: Predicción con datos faltantes
    print("\n6. Probando predicción con datos faltantes")
    invalid_data = {
        "PhysicalActivities": "1",
        "AlcoholDrinkers": "0"
        # Falta el resto de campos
    }
    test_endpoint(f"{BASE_URL}/predict", method="POST", data=invalid_data, expected_status=400)
    
    # Test 7: Predicción con valores inválidos
    print("\n7. Probando predicción con valores inválidos")
    invalid_values = {
        "PhysicalActivities": "5",  # Valor inválido
        "AlcoholDrinkers": "0",
        "ageCategoryGrouped": "1",
        "SmokerStatusGrouped": "0",
        "HadDiabetesGrouped": "0",
        "HadHeartAttack": "0"
    }
    test_endpoint(f"{BASE_URL}/predict", method="POST", data=invalid_values, expected_status=400)
    
    print("\n" + "=" * 50)
    print("🎉 Pruebas completadas!")
    print("\nPara probar la interfaz web, visite: http://127.0.0.1:5000")

if __name__ == "__main__":
    # Esperar un poco para que el servidor esté listo
    print("Esperando que el servidor esté listo...")
    time.sleep(2)
    
    run_tests()
