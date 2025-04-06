from fastapi import FastAPI, Query
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from rapidfuzz import process
from data import properties
import time

app = FastAPI()
geolocator = Nominatim(user_agent="moustache_api")

# Pre-build list of cities/states for better fuzzy matching
search_pool = list(set([
    "Udaipur", "Jaipur", "Jaisalmer", "Jodhpur", "Agra", "Delhi", "Rishikesh", "Varanasi", 
    "Goa", "Koksar", "Daman", "Pushkar", "Khajuraho", "Manali", "Bhimtal", "Srinagar", 
    "Ranthambore", "Coimbatore", "Shoja", "Sissu"
]))

def fuzzy_match_location(user_input: str):
    match, score, _ = process.extractOne(user_input, search_pool)
    return match if score > 60 else user_input

@app.get("/nearest-property")
def nearest_property(query: str = Query(..., description="City, state, or area (can include minor typos)")):
    start_time = time.time()

    # Step 1: Fuzzy match to correct user typo
    corrected_query = fuzzy_match_location(query)

    # Step 2: Get latitude and longitude of the corrected query
    location = geolocator.geocode(corrected_query)
    if not location:
        return {"error": f"Location '{query}' not recognized."}

    user_coords = (location.latitude, location.longitude)

    # Step 3: Find closest property within 50km
    nearest = None
    min_distance = float('inf')

    for prop in properties:
        prop_coords = (prop["latitude"], prop["longitude"])
        distance_km = geodesic(user_coords, prop_coords).km
        if distance_km <= 50 and distance_km < min_distance:
            min_distance = distance_km
            nearest = {
                "property": prop["name"],
                "distance_km": round(distance_km, 2)
            }

    if nearest:
        return {
            "location": corrected_query,
            "nearest_property": nearest["property"],
            "distance_km": nearest["distance_km"],
            "response_time_sec": round(time.time() - start_time, 2)
        }
    else:
        return {
            "location": corrected_query,
            "message": "No properties available within 50km.",
            "response_time_sec": round(time.time() - start_time, 2)
        }
