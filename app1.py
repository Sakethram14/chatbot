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


# --- Section 2: Agent Logic (No changes to these functions) ---
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
        # --- FIX #1: Corrected the secret name to match secrets.toml ---
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
    except requests.exceptions.RequestException as e:
        return f"Error getting access token: {e}"

    model_id = "ibm/granite-13b-instruct-v2"
    context = retrieve_context(user_query)
    
    prompt = f"""
    You are an expert Travel Planner Agent. Your task is to create a personalized travel itinerary based on the user's request and the provided context.
    **Context from Knowledge Base:**
    ---
    {context}
    ---
    **User's Request:**
    "{user_query}"
    **Instructions:**
    - Analyze the user's request for details like destination, duration, budget, and interests.
    - Use **only** the information from the provided context to suggest a plan.
    - Create a clear, day-by-day itinerary.
    - If the context includes hotel and activity suggestions, incorporate them into the plan.
    - If the user's budget is 'budget', recommend budget-friendly options from the context. Do the same for 'luxury' or 'mid-range'.
    - If no specific city is found in the context, create a generic travel plan for one of the available cities.
    - Present the final output in a clean, readable format. Do not mention the context or the prompt in your response. Start directly with the travel plan.
    **Generated Itinerary:**
    """

    # --- FIX #2: Corrected the region to match your project's location (Sydney) ---
    generation_url = "https://au-syd.ml.cloud.ibm.com/ml/v1/text/generation?version=2024-04-01"
    generation_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    generation_payload = {
        "model_id": model_id,
        "input": prompt,
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 400,
            "min_new_tokens": 50,
            "repetition_penalty": 1.1
        },
        "project_id": project_id
    }

    try:
        generation_response = requests.post(generation_url, headers=generation_headers, json=generation_payload)
        generation_response.raise_for_status()
        response_json = generation_response.json()
        return response_json['results'][0]['generated_text']
    except requests.exceptions.RequestException as e:
        return f"Error calling generation API: {e}\nResponse: {generation_response.text}"

# --- Section 3: Streamlit User Interface (MODIFIED FOR CHATBOT) ---
st.set_page_config(page_title="AI Travel Planner Chatbot", layout="centered")
st.title("🌍 AI Travel Planner Chatbot")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get new user input
if prompt := st.chat_input("Tell me about your dream trip..."):
    # Add user message to history and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and display AI response
    with st.chat_message("assistant"):
        with st.spinner("🤖 Crafting your personalized journey..."):
            response = generate_plan(prompt)
            st.markdown(response)
    
    # Add AI response to history
    st.session_state.messages.append({"role": "assistant", "content": response})
