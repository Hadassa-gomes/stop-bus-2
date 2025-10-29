from typing import Dict, Any
from datetime import datetime
import math

def clean_reading(temperature: Any, humidity: Any) -> Dict[str, Any]:
    """Limpa e valida dados do sensor"""
    
    # 1. Valores obrigatórios
    if temperature is None or humidity is None:
        raise ValueError("Temperature and humidity are required")
    
    # 2. Conversão para float
    try:
        temp = float(temperature)
        hum = float(humidity)
    except (ValueError, TypeError):
        raise ValueError("Invalid numeric values")
    
    # 3. Validação NaN/Inf
    if math.isnan(temp) or math.isnan(hum) or math.isinf(temp) or math.isinf(hum):
        raise ValueError("Invalid reading (NaN/Inf)")
    
    # 4. Intervalos físicos
    if not (-40 <= temp <= 80):
        raise ValueError(f"Temperature out of range: {temp}")
    if not (0 <= hum <= 100):
        raise ValueError(f"Humidity out of range: {hum}")
    
    # 5. Arredondamento
    temp = round(temp, 2)
    hum = round(hum, 2)
    
    return {
        "temperature_celsius": temp,
        "humidity_percent": hum,
        "recorded_at": datetime.utcnow()
    }