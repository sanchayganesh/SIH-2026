from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__, template_folder='.')
CORS(app)  # Enables frontend requests from index.html / index2.html

ATTRACTIONS = {
    "Delhi": [
        {"name": "Red Fort", "cost": 50, "time": "Morning", "image": "https://images.unsplash.com/photo-1587474260584-136574528ed5?w=500"},
        {"name": "Qutub Minar", "cost": 40, "time": "Afternoon", "image": "https://images.unsplash.com/photo-1565352195254-8e4a7873832c?w=500"},
        {"name": "Lotus Temple", "cost": 0, "time": "Evening", "image": "https://images.unsplash.com/photo-1595846519845-68e298c2edd8?w=500"},
        {"name": "India Gate", "cost": 0, "time": "Evening", "image": "https://images.unsplash.com/photo-1599661046827-dacff0c0f09a?w=500"},
        {"name": "Kingdom of Dreams", "cost": 1200, "time": "Full Day", "image": "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=500"}
    ],
    "Mumbai": [
        {"name": "Gateway of India", "cost": 0, "time": "Morning", "image": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?w=500"},
        {"name": "Elephanta Caves", "cost": 260, "time": "Afternoon", "image": "https://images.unsplash.com/photo-1605649487212-47bdab06cf3f?w=500"},
        {"name": "Marine Drive", "cost": 0, "time": "Evening", "image": "https://images.unsplash.com/photo-1566552881560-0be862a7c445?w=500"},
        {"name": "EsselWorld", "cost": 1050, "time": "Full Day", "image": "https://images.unsplash.com/photo-1513889961551-628c1e5e2ee9?w=500"}
    ],
    "Bengaluru": [
        {"name": "Cubbon Park", "cost": 0, "time": "Morning", "image": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=500"},
        {"name": "Bengaluru Palace", "cost": 400, "time": "Afternoon", "image": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?w=500"},
        {"name": "Visvesvaraya Museum", "cost": 100, "time": "Evening", "image": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=500"},
        {"name": "Wonderla", "cost": 1400, "time": "Full Day", "image": "https://images.unsplash.com/photo-1513889961551-628c1e5e2ee9?w=500"}
    ],
    "Kolkata": [
        {"name": "Victoria Memorial", "cost": 50, "time": "Morning", "image": "https://images.unsplash.com/photo-1558431382-27e303142255?w=500"},
        {"name": "Howrah Bridge", "cost": 0, "time": "Evening", "image": "https://images.unsplash.com/photo-1571679650686-981882672b1a?w=500"},
        {"name": "Indian Museum", "cost": 50, "time": "Afternoon", "image": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=500"}
    ],
    "Chennai": [
        {"name": "Marina Beach", "cost": 0, "time": "Morning", "image": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?w=500"},
        {"name": "Kapaleeshwarar Temple", "cost": 0, "time": "Morning", "image": "https://images.unsplash.com/photo-1609946782701-7ed82a170588?w=500"},
        {"name": "Government Museum", "cost": 50, "time": "Afternoon", "image": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=500"}
    ],
    "Hyderabad": [
        {"name": "Charminar", "cost": 25, "time": "Morning", "image": "https://images.unsplash.com/photo-1605649487212-47bdab06cf3f?w=500"},
        {"name": "Golconda Fort", "cost": 25, "time": "Afternoon", "image": "https://images.unsplash.com/photo-1609946782701-7ed82a170588?w=500"},
        {"name": "Ramoji Film City", "cost": 1350, "time": "Full Day", "image": "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=500"}
    ],
    "Ahmedabad": [
        {"name": "Sabarmati Ashram", "cost": 0, "time": "Morning", "image": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?w=500"},
        {"name": "Adalaj Stepwell", "cost": 0, "time": "Afternoon", "image": "https://images.unsplash.com/photo-1605649487212-47bdab06cf3f?w=500"},
        {"name": "Kankaria Lake", "cost": 20, "time": "Evening", "image": "https://images.unsplash.com/photo-1566552881560-0be862a7c445?w=500"}
    ],
    "Pune": [
        {"name": "Shaniwar Wada", "cost": 25, "time": "Morning", "image": "https://images.unsplash.com/photo-1609946782701-7ed82a170588?w=500"},
        {"name": "Aga Khan Palace", "cost": 25, "time": "Afternoon", "image": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?w=500"},
        {"name": "Sinhagad Fort", "cost": 50, "time": "Morning", "image": "https://images.unsplash.com/photo-1605649487212-47bdab06cf3f?w=500"}
    ]
}

# Serve Main Page
@app.route('/')
def home():
    return render_template('index.html')

# Route 2: Serves Second Webpage (Tracker/Results)
@app.route('/index2.html')
def results():
    return render_template('index2.html')

# API Route
@app.route('/generate-itinerary', methods=['POST'])
def generate_itinerary():
    data = request.json
    city = data.get('city', '').capitalize()
    budget = float(data.get('budget', 0))
    days = int(data.get('days', 1))
    members = int(data.get('members', 1))

    per_person_daily_budget = (budget / members) / days if (members > 0 and days > 0) else 0

    matched_city_key = next((k for k in ATTRACTIONS if k.lower() == city.lower()), None)
    
    if not matched_city_key:
        return jsonify({"error": f"City '{city}' not found in database"}), 404

    city_spots = ATTRACTIONS[matched_city_key]

    if per_person_daily_budget < 100:
        available_spots = [s for s in city_spots if s['cost'] <= 50]
    elif per_person_daily_budget < 500:
        available_spots = [s for s in city_spots if s['cost'] <= 300]
    else:
        available_spots = city_spots

    if not available_spots:
        available_spots = city_spots

    itinerary = []
    spot_idx = 0
    total_spots = len(available_spots)

    for day in range(1, days + 1):
        day_plan = {"day": f"Day {day}", "places": []}
        for _ in range(2):
            day_plan["places"].append(available_spots[spot_idx % total_spots])
            spot_idx += 1
        itinerary.append(day_plan)

    return jsonify({
        "city": matched_city_key,
        "days": days,
        "members": members,
        "daily_per_person_budget": round(per_person_daily_budget, 2),
        "itinerary": itinerary
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
