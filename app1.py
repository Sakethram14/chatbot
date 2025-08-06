import streamlit as st
import pandas as pd
import io
import requests
import json

# --- Section 1: Data Loading (No changes here) ---
destinations_data = """City,Country,Description,BestTimeToVisit,Interests
Paris,France,"The city of light, known for its art, fashion, and iconic landmarks like the Eiffel Tower.",Spring or Fall,"Art,History,Food,Romance"
Tokyo,Japan,"A bustling metropolis where modern technology coexists with ancient traditions.",Spring or Fall,"Technology,Food,Culture,Anime"
Rome,Italy,"An ancient city filled with historical ruins, Renaissance art, and world-class cuisine.",Spring or Summer,"History,Art,Food,Architecture"
Kyoto,Japan,"Japan's former imperial capital, famous for its beautiful temples, gardens, and traditional geisha districts.",Spring or Fall,"Culture,History,Nature,Relaxation"
New York,USA,"The city that never sleeps, a global hub for finance, art, and entertainment.",Anytime,"Entertainment,Shopping,Food,Theatre"
"""
hotels_data = """City,HotelName,PriceRange,Rating
Paris,Le Bristol Paris,Luxury,5
Paris,Hotel Henriette,Mid-range,4
Paris,The People Paris Belleville,Budget,3
Tokyo,Park Hyatt Tokyo,Luxury,5
Tokyo,Shibuya Granbell Hotel,Mid-range,4
Tokyo,Khaosan Tokyo Samurai,Budget,3
Rome,Hotel Hassler Roma,Luxury,5
Rome,Trastevere's Friends,Mid-range,4
Rome,The Beehive,Budget,3
"""
activities_data = """City,ActivityName,Type,Description
Paris,Visit the Louvre Museum,Museum,"Home to masterpieces like the Mona Lisa."
Paris,Seine River Cruise,Tour,"A relaxing way to see the city's landmarks."
Paris,Boulangerie Tour,Food,"Sample some of the best bread and pastries in the world."
Tokyo,Shibuya Crossing,Landmark,"Experience the world's busiest pedestrian intersection."
Tokyo,TeamLab Borderless,Museum,"An immersive digital art museum that blurs the line between art and technology."
Tokyo,Sushi Making Class,Food,"Learn the art of sushi from a master chef."
Rome,Colosseum Tour,History,"Explore the ancient amphitheater that once hosted gladiator contests."
Rome,Vatican City Visit,History,"Visit St. Peter's Basilica and the Sistine Chapel."
Rome,Pasta Making Class,Food,"Learn how to make authentic Italian pasta from scratch."
"""
df_destinations = pd.read_csv(io.StringIO(destinations_data))
df_hotels = pd.read_csv(io.StringIO(hotels_data))
df_activities = pd.read_csv(io.StringIO(activities_data))


# --- Section 2: Agent Logic (No changes here) ---
def retrieve_context(query):
    context_parts = []
    query_lower = query.lower()
    for city in df_destinations['City']:
        if city.lower() in query_lower:
            context_parts.append(f"Destination Info:\n{df_destinations[df_destinations['City'] == city].to_string()}")
            context_parts.append(f"\nHotel Info:\n{df_hotels[df_hotels['City'] == city].to_string()}")
            context_parts.append(f"\nActivity Info:\n{df_activities[df_activities['City'] == city].to_string()}")
    if not context_parts:
        return "No specific city information found. Provide a general plan."
    return "\n\n".join(context_parts)

def generate_plan(user_query):
    """
    Generates a travel plan by calling the IBM Watsonx.ai API directly.
    """
    try:
        api_key = st.secrets["WATSONX_API_KEY"]
        project_id = st.secrets["WATSONX_PROJECT_ID"]
    except FileNotFoundError:
        return "Error: Secrets file not found. This app must be deployed on Streamlit Community Cloud with secrets configured."

    token_url = "https://iam.cloud.ibm.com/identity/token"
    token_headers = {"Content-Type": "application/x-www-form-urlencoded"}
    token_data = f"grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey={api_key}"
    
    try:
        token_response = requests.post(token_url, headers=token_headers, data=token_data)
        token_response.raise_for_status()
        access_token = token_response.json()["access_token"]
    except requests.
