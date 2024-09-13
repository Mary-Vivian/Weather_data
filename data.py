import random
import csv
from datetime import datetime, timedelta
def generate_simulated_weather(start_date, end_date, lat, lon):
    current_date = start_date
    weather_data = []
    while current_date <= end_date:
        month = current_date.month
        if 3 <= month <= 5 or 10 <= month <= 12:
            rainfall_1h = random.uniform(0, 10)
            rainfall_3h = rainfall_1h * 3 + random.uniform(0, 5)
            precipitation_prob = random.uniform(0.3, 0.8)
            humidity = random.uniform(60, 90)
            temperature = random.uniform(18, 28)
        else:
            rainfall_1h = random.uniform(0, 2)
            rainfall_3h = rainfall_1h * 3 + random.uniform(0, 1)
            precipitation_prob = random.uniform(0, 0.3)
            humidity = random.uniform(40, 70)
            temperature = random.uniform(15, 25)
        weather_data.append({
            "date_time": current_date.strftime("%Y-%m-%d %H:%M:%S"),
            "rainfall_1h": round(rainfall_1h, 2),
            "rainfall_3h": round(rainfall_3h, 2),
            "precipitation_prob": round(precipitation_prob, 2),
            "humidity": round(humidity, 2),
            "temperature": round(temperature, 2),
            "latitude": lat,
            "longitude": lon
        })
        current_date += timedelta(days=1)
    return weather_data
nairobi_wards = [
    {"name": "Westlands", "lat": -1.2687, "lon": 36.8105},
    {"name": "Dagoretti", "lat": -1.2889, "lon": 36.7444},
    {"name": "Langata", "lat": -1.3504, "lon": 36.7344},
    {"name": "Kibra", "lat": -1.3122, "lon": 36.7842},
    {"name": "Roysambu", "lat": -1.2187, "lon": 36.8844},
    {"name": "Kasarani", "lat": -1.2211, "lon": 36.8987},
    {"name": "Ruaraka", "lat": -1.2475, "lon": 36.8872},
    {"name": "Embakasi", "lat": -1.3028, "lon": 36.8938},
    {"name": "Makadara", "lat": -1.2906, "lon": 36.8575},
    {"name": "Kamukunji", "lat": -1.2833, "lon": 36.8500},
    {"name": "Starehe", "lat": -1.2811, "lon": 36.8272},
    {"name": "Mathare", "lat": -1.2583, "lon": 36.8573},
]
start_date = datetime(2020, 1, 1)
end_date = datetime(2022, 12, 31)
simulated_data = {}
for ward in nairobi_wards:
    simulated_data[ward["name"]] = generate_simulated_weather(start_date, end_date, ward["lat"], ward["lon"])
openweather_url = "https://openweathermap.org/"
with open('dat.csv', 'w', newline='') as csvfile:
    fieldnames = ['ward', 'date_time', 'rainfall_1h', 'rainfall_3h', 'precipitation_prob', 'humidity', 'temperature', 'latitude', 'longitude', 'source_url']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for ward_name, data in simulated_data.items():
        for entry in data:
            row = {'ward': ward_name, **entry, 'source_url': openweather_url}
            writer.writerow(row)
print("Data has been successfully written to dat.csv")
print("\nAverage Yearly Weather Statistics:")
for ward_name, data in simulated_data.items():
    yearly_totals = {year: {'rainfall': 0, 'temp': 0, 'humidity': 0, 'count': 0} for year in range(2020, 2023)}
    for entry in data:
        year = datetime.strptime(entry['date_time'], "%Y-%m-%d %H:%M:%S").year
        yearly_totals[year]['rainfall'] += entry['rainfall_1h']
        yearly_totals[year]['temp'] += entry['temperature']
        yearly_totals[year]['humidity'] += entry['humidity']
        yearly_totals[year]['count'] += 1
    avg_yearly_rainfall = sum(year_data['rainfall'] for year_data in yearly_totals.values()) / len(yearly_totals)
    avg_yearly_temp = sum(year_data['temp'] / year_data['count'] for year_data in yearly_totals.values()) / len(yearly_totals)
    avg_yearly_humidity = sum(year_data['humidity'] / year_data['count'] for year_data in yearly_totals.values()) / len(yearly_totals)
    print(f"{ward_name}: Rainfall: {avg_yearly_rainfall:.2f} mm, Temperature: {avg_yearly_temp:.2f}°C, Humidity: {avg_yearly_humidity:.2f}%")
