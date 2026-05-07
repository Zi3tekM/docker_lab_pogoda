import os
from datetime import datetime
from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)
PORT = 5000
AUTHOR = "Michał Ziętek"

# Logi informacjyjne przy starcie aplikacji
print(f"--- LOGI STARTOWE ---")
print(f"Data uruchomienia: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Autor: {AUTHOR}")
print(f"Port TCP: {PORT}")
print(f"---------------------")

# Słownik danych: Kraje i przypisane do nich miasta ze współrzędnymi
LOCATIONS = {
    "Polska": {
        "Warszawa": "52.23,21.01",
        "Kraków": "50.06,19.94",
        "Lublin": "51.25,22.57"
    },
    "Niemcy": {
        "Berlin": "52.52,13.40",
        "Monachium": "48.13,11.57",
        "Hamburg": "53.55,9.99"
    },
    "Francja": {
        "Paryż": "48.85,2.35",
        "Lyon": "45.76,4.83",
        "Marsylia": "43.29,5.37"
    }
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <title>Monitor Pogody OCI</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f0f2f5; color: #333; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
        .container { background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); width: 100%; max-width: 400px; text-align: center; }
        h1 { color: #1a73e8; margin-bottom: 0.5rem; }
        .author { font-size: 0.9rem; color: #666; margin-bottom: 2rem; }
        select, button { width: 100%; padding: 10px; margin: 10px 0; border-radius: 6px; border: 1px solid #ddd; font-size: 1rem; }
        button { background-color: #1a73e8; color: white; border: none; cursor: pointer; font-weight: bold; transition: background 0.3s; }
        button:hover { background-color: #1557b0; }
        .weather-box { margin-top: 2rem; padding: 1rem; background: #e8f0fe; border-radius: 8px; border: 1px solid #d2e3fc; }
        .temp { font-size: 2.5rem; font-weight: bold; color: #1a73e8; }
        .info { margin: 5px 0; font-size: 1.1rem; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Pogoda Cloud App</h1>
        <p class="author">Autor: {{ author }}</p>
        
        <form method="POST">
            <select name="country" onchange="this.form.submit()">
                <option value="">-- Wybierz kraj --</option>
                {% for c in locations.keys() %}
                <option value="{{ c }}" {% if selected_country == c %}selected{% endif %}>{{ c }}</option>
                {% endfor %}
            </select>

            {% if selected_country %}
            <select name="city">
                <option value="">-- Wybierz miasto --</option>
                {% for city_name, coords in locations[selected_country].items() %}
                <option value="{{ city_name }}|{{ coords }}">{{ city_name }}</option>
                {% endfor %}
            </select>
            <button type="submit">Sprawdź pogodę</button>
            {% endif %}
        </form>

        {% if weather %}
        <div class="weather-box">
            <h3>{{ city_label }}</h3>
            <div class="temp">{{ weather.temp }}°C</div>
            <p class="info"> Wilgotność: <strong>{{ weather.hum }}%</strong></p>
            <p class="info"> Wiatr: <strong>{{ weather.wind }} km/h</strong></p>
            <p class="info">️ Ciśnienie: <strong>{{ weather.press }} hPa</strong></p>
            <p class="info">️ Opady: <strong>{{ weather.rain }} mm</strong></p>
            <p class="info">️ Zachmurzenie: <strong>{{ weather.clouds }}%</strong></p>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""


@app.route('/', methods=['GET', 'POST'])
def index():
    selected_country = request.form.get('country')
    weather_data = None
    city_label = None

    if request.method == 'POST' and 'city' in request.form:
        city_info = request.form.get('city').split('|')
        if len(city_info) == 2:
            city_label = city_info[0]
            coords = city_info[1].split(',')
            
            # Zapytanie API o temperaturę, wilgotność, wiatr, ciśnienie, opady i zachmurzenie
            url = f"https://api.open-meteo.com/v1/forecast?latitude={coords[0]}&longitude={coords[1]}&current=temperature_2m,relative_humidity_2m,surface_pressure,precipitation,cloud_cover,wind_speed_10m"
            res = requests.get(url)
            
            if res.status_code == 200:
                curr = res.json().get('current', {})
                weather_data = {
                    "temp": curr.get('temperature_2m'),
                    "hum": curr.get('relative_humidity_2m'),
                    "wind": curr.get('wind_speed_10m'),
                    "press": curr.get('surface_pressure'),
                    "rain": curr.get('precipitation'),
                    "clouds": curr.get('cloud_cover')
                }
    
    return render_template_string(
        HTML_TEMPLATE, 
        author=AUTHOR, 
        locations=LOCATIONS, 
        selected_country=selected_country,
        weather=weather_data,
        city_label=city_label
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)