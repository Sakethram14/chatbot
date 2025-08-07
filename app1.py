import streamlit as st
import pandas as pd
import io
import re
# Import the official IBM library
from ibm_watson_machine_learning.foundation_models import Model

# --- Section 1: Data Loading (Unchanged) ---
destinations_data = """City,Country,Description,BestTimeToVisit,Interests
Paris,France,"The city of light, known for its art, fashion, and iconic landmarks like the Eiffel Tower.",Spring or Fall,"Art,History,Food,Romance"
Tokyo,Japan,"A bustling metropolis where modern technology coexists with ancient traditions.",Spring or Fall,"Technology,Food,Culture,Anime"
Rome,Italy,"An ancient city filled with historical ruins, Renaissance art, and world-class cuisine.",Spring or Summer,"History,Art,Food,Architecture"
Kyoto,Japan,"Japan's former imperial capital, famous for its beautiful temples, gardens, and traditional geisha districts.",Spring or Fall,"Culture,History,Nature,Relaxation"
New York,USA,"The city that never sleeps, a global hub for finance, art, and entertainment.",Anytime,"Entertainment,Shopping,Food,Theatre"
Delhi,India,"India's capital, a sprawling metropolis that blends ancient Mughal history with a modern, cosmopolitan pulse.",October to March,"History,Food,Shopping,Culture"
Goa,India,"A coastal paradise famous for its sun-kissed beaches, vibrant nightlife, and Portuguese heritage.",November to February,"Beaches,Nightlife,Relaxation,Watersports"
Jaipur,India,"The Pink City, renowned for its magnificent forts, opulent palaces, and bustling, colorful markets.",October to March,"History,Architecture,Shopping,Culture"
Kerala,India,"'God's Own Country', a serene region of tranquil backwaters, lush tea plantations, and spice-scented air.",September to March,"Nature,Relaxation,Houseboats,Wellness"
London,UK,"A historic global city, home to royalty, iconic landmarks like the Tower Bridge, and world-class museums.",Summer,"History,Culture,Theatre,Shopping"
Sydney,Australia,"Known for its spectacular harbour, iconic Opera House, and famous beaches like Bondi.",Spring or Fall,"Landmarks,Beaches,Outdoors,Food"
Dubai,UAE,"A futuristic desert oasis of superlatives, featuring the world's tallest building, luxury shopping, and bold architecture.",Winter,"Modern,Shopping,Luxury,Adventure"
Varanasi,India,"One of the world's oldest living cities, considered the spiritual capital of India, on the banks of the Ganges.",October to March,"Spiritual,Culture,History,River"
Mumbai,India,"India's bustling financial powerhouse, home to the Bollywood film industry and colonial architecture.",October to February,"Entertainment,Food,History,City Life"
Udaipur,India,"The 'City of Lakes', known for its romantic lakeside palaces, historic forts, and gardens.",September to March,"Romance,History,Architecture,Lakes"
Rishikesh,India,"The 'Yoga Capital of the World', nestled in the Himalayas on the banks of the Ganges, offering adventure and spirituality.",September to June,"Yoga,Adventure,Spiritual,Nature"
Shimla,India,"The former summer capital of British India, a popular Himalayan hill station with colonial architecture.",March to June,"Mountains,Colonial,Nature,Relaxation"
Bangkok,Thailand,"A vibrant city known for its ornate shrines, bustling street life, and world-famous street food.",November to February,"Food,Culture,Nightlife,Temples"
Singapore,Singapore,"A futuristic city-state and island country, famous for its green spaces, modern architecture, and multicultural food scene.",Anytime,"Modern,Family,Food,Gardens"
Amsterdam,Netherlands,"Known for its artistic heritage, elaborate canal system, and narrow houses with gabled facades.",April to May or September to November,"Art,Canals,Culture,History"
Cairo,Egypt,"Egypt's sprawling capital, set on the Nile River, with nearby Giza being the site of the iconic pyramids and the Great Sphinx.",October to April,"History,Ancient,Culture,Museum"
Rio de Janeiro,Brazil,"A huge seaside city in Brazil, famed for its Copacabana and Ipanema beaches, Christ the Redeemer statue, and Carnival festival.",September to October or December to March,"Beaches,Nature,Landmarks,Nightlife"
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
Delhi,The Imperial,Luxury,5
Delhi,The Lalit,Mid-range,4
Delhi,Zostel Delhi,Budget,3
Goa,Taj Exotica,Luxury,5
Goa,The Park Baga River,Mid-range,4
Goa,The Funky Monkey Hostel,Budget,3
Jaipur,Rambagh Palace,Luxury,5
Jaipur,Samode Haveli,Mid-range,4
Jaipur,Moustache Hostel,Budget,3
Kerala,Kumarakom Lake Resort,Luxury,5
Kerala,Marari Beach Resort,Mid-range,4
Kerala,The Lost Hostels Varkala,Budget,3
London,The Savoy,Luxury,5
London,The Hoxton Shoreditch,Mid-range,4
London,Generator London,Budget,3
Sydney,Park Hyatt Sydney,Luxury,5
Sydney,Ovolo Woolloomooloo,Mid-range,4
Sydney,Wake Up! Sydney Central,Budget,3
Dubai,Burj Al Arab,Luxury,5
Dubai,Rove Downtown,Mid-range,4
Dubai,Rove Dubai Marina,Budget,3
Varanasi,BrijRama Palace,Luxury,5
Varanasi,Dwivedi Hotels Palace on Steps,Mid-range,4
Varanasi,goStops Varanasi,Budget,3
Mumbai,The Taj Mahal Palace,Luxury,5
Mumbai,Trident Nariman Point,Mid-range,4
Mumbai,Abode Bombay,Budget,3
Udaipur,The Oberoi Udaivilas,Luxury,5
Udaipur,Amet Haveli,Mid-range,4
Udaipur,Zostel Udaipur,Budget,3
Rishikesh,Ananda in the Himalayas,Luxury,5
Rishikesh,Aloha on the Ganges,Mid-range,4
Rishikesh,Zostel Rishikesh,Budget,3
Shimla,Wildflower Hall,Luxury,5
Shimla,The Oberoi Cecil,Mid-range,4
Shimla,Clarkes Hotel,Budget,3
Bangkok,Mandarin Oriental,Luxury,5
Bangkok,Ariyasomvilla,Mid-range,4
Bangkok,The Yard Hostel,Budget,3
Singapore,Marina Bay Sands,Luxury,5
Singapore,The Fullerton Hotel,Mid-range,4
Singapore,The Pod @ Beach Road,Budget,3
Amsterdam,Waldorf Astoria Amsterdam,Luxury,5
Amsterdam,The Hoxton Amsterdam,Mid-range,4
Amsterdam,Flying Pig Downtown,Budget,3
Cairo,Four Seasons Hotel Cairo,Luxury,5
Cairo,Kempinski Nile Hotel,Mid-range,4
Cairo,The Australian Hostel,Budget,3
Rio de Janeiro,Belmond Copacabana Palace,Luxury,5
Rio de Janeiro,Yoo2 Rio de Janeiro,Mid-range,4
Rio de Janeiro,Selina Lapa Rio,Budget,3
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
Delhi,Visit India Gate & Rajpath,History,"Pay respects at the war memorial and see the heart of New Delhi."
Delhi,Explore Qutub Minar,History,"Marvel at the towering minaret and surrounding ancient ruins."
Delhi,Chandni Chowk Food Walk,Food,"Taste the chaotic and delicious street food of Old Delhi."
Goa,Relax at Palolem Beach,Beach,"Enjoy the serene, crescent-shaped beach lined with coconut palms."
Goa,Explore Old Goa Churches,History,"Visit the UNESCO World Heritage sites like the Basilica of Bom Jesus."
Goa,Dudhsagar Falls Trip,Nature,"Witness the majestic 'Sea of Milk' waterfall on the Mandovi River."
Jaipur,Tour Amer Fort,History,"Explore the magnificent hilltop fort overlooking Maota Lake."
Jaipur,Photo at Hawa Mahal,Architecture,"See the iconic 'Palace of Winds' with its intricate latticework."
Jaipur,Shop at Johari Bazaar,Shopping,"Bargain for gemstones, textiles, and traditional Rajasthani crafts."
Kerala,Alleppey Backwater Cruise,Houseboat,"Spend a day or night on a traditional houseboat, a unique Kerala experience."
Kerala,Visit a Munnar Tea Garden,Nature,"Walk through lush green tea plantations and learn about tea processing."
Kerala,Relax on Varkala Beach,Beach,"Unwind on the cliff-top beach known for its stunning sunsets and natural springs."
London,Tour the Tower of London,History,"Discover the history of the Crown Jewels, ravens, and Yeoman Warders."
London,Ride the London Eye,Landmark,"Get a panoramic view of the city from the giant Ferris wheel."
London,Watch a West End Show,Theatre,"Experience world-class theatre in London's famous theatre district."
Sydney,Sydney Opera House Tour,Landmark,"Go inside the iconic sails and learn about its history and architecture."
Sydney,Relax or Surf at Bondi Beach,Beach,"Visit Australia's most famous beach for sun, sand, and surf."
Sydney,Climb the Harbour Bridge,Adventure,"Take a guided climb for breathtaking views of the city and harbour."
Dubai,Visit At the Top - Burj Khalifa,Landmark,"Ascend the world's tallest building for unparalleled city views."
Dubai,Evening Desert Safari,Adventure,"Experience dune bashing, camel rides, and a traditional Bedouin dinner."
Dubai,Explore the Dubai Mall,Shopping,"Shop at one of the world's largest malls, featuring an aquarium and ice rink."
Varanasi,Ganga Aarti Ceremony,Spiritual,"Witness the spectacular evening prayer ritual on the banks of the Ganges."
Varanasi,Sunrise Boat Ride,River,"Experience a peaceful boat ride on the Ganges at dawn to see the city awaken."
Varanasi,Explore the Ghats and Alleys,Culture,"Wander through the ancient, narrow lanes and the famous riverside steps."
Mumbai,Visit the Gateway of India,Landmark,"See the iconic arch-monument overlooking the Arabian Sea."
Mumbai,Walk along Marine Drive,Relaxation,"Enjoy a sunset stroll along the 'Queen's Necklace' promenade."
Mumbai,Explore Elephanta Caves,History,"Take a ferry to see the ancient rock-cut cave temples."
Udaipur,Boat Ride on Lake Pichola,Lake,"Enjoy a scenic boat tour with views of the City Palace and Jag Mandir."
Udaipur,Visit the City Palace,History,"Explore the vast palace complex, a blend of Rajasthani and Mughal architecture."
Udaipur,Explore Saheliyon-ki-Bari,Nature,"Stroll through the beautiful 'Garden of the Maidens' with its fountains and kiosks."
Rishikesh,White Water Rafting,Adventure,"Experience thrilling rapids on the River Ganges."
Rishikesh,Attend a Yoga Retreat,Yoga,"Immerse yourself in yoga and meditation at an ashram in the 'Yoga Capital'."
Rishikesh,Visit Laxman Jhula,Landmark,"Walk across the iconic suspension bridge with stunning river and mountain views."
Shimla,Walk The Mall Road,Shopping,"Stroll along the main street of Shimla, lined with shops and cafes."
Shimla,Ride the Kalka-Shimla Toy Train,Train,"Experience a scenic journey on the UNESCO World Heritage railway."
Shimla,Visit the Jakhu Temple,Spiritual,"Hike or take a cable car to the temple dedicated to the monkey god Hanuman."
Bangkok,Visit the Grand Palace,Temple,"Marvel at the opulent architecture of the former royal residence."
Bangkok,Chatuchak Weekend Market,Shopping,"Get lost in one of the world's largest outdoor markets."
Bangkok,Street Food Tour,Food,"Sample a wide variety of delicious and authentic Thai street food."
Singapore,Explore Gardens by the Bay,Gardens,"Visit the futuristic Supertree Grove and the stunning climate-controlled biodomes."
Singapore,Visit Sentosa Island,Entertainment,"Enjoy theme parks, beaches, and various attractions on this resort island."
Singapore,Eat at a Hawker Centre,Food,"Experience Singapore's diverse food culture at an affordable open-air food court."
Amsterdam,Visit the Rijksmuseum,Art,"See masterpieces by Rembrandt, Vermeer, and other Dutch masters."
Amsterdam,Take a Canal Cruise,Canals,"Explore the city's scenic canals and historic architecture from the water."
Amsterdam,Explore the Anne Frank House,History,"Visit the secret annex where Anne Frank and her family hid during WWII."
Cairo,Visit the Pyramids of Giza,Ancient,"Stand in awe of the last remaining wonder of the ancient world."
Cairo,Explore the Egyptian Museum,Museum,"Discover the world's most extensive collection of ancient Egyptian artifacts."
Cairo,Shop at Khan el-Khalili Bazaar,Shopping,"Haggle for souvenirs, spices, and crafts in the historic souk."
Rio de Janeiro,Visit Christ the Redeemer,Landmark,"Take a train up Corcovado mountain to the iconic statue for panoramic views."
Rio de Janeiro,Ride Sugarloaf Mountain Cable Car,Nature,"Enjoy breathtaking 360-degree views of the city and its surroundings."
Rio de Janeiro,Relax on Copacabana Beach,Beach,"Soak up the sun on one of the most famous beaches in the world."
"""
df_destinations = pd.read_csv(io.StringIO(destinations_data))
df_hotels = pd.read_csv(io.StringIO(hotels_data))
df_activities = pd.read_csv(io.StringIO(activities_data))


# --- Section 2: Agent Logic (NOW USING IBM'S OFFICIAL PYTHON LIBRARY) ---
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
    Generates a travel plan using the official ibm-watson-machine-learning library.
    This is the most reliable method and bypasses issues with the website UI.
    """
    try:
        api_key = st.secrets["WATSONX_API_KEY"]
        project_id = st.secrets["WATSONX_PROJECT_ID"]
    except Exception as e:
        return f"Error: Make sure you have created secrets.toml with WATSONX_API_KEY and WATSONX_PROJECT_ID. Details: {e}"

    # These are the credentials for the Dallas region.
    # The library uses the base URL, not the full endpoint.
    credentials = {
        "url": "https://us-south.ml.cloud.ibm.com",
        "apikey": api_key
    }

    # Define model parameters
    model_id = "ibm/granite-13b-instruct-v2"
    parameters = {
        "decoding_method": "greedy",
        "max_new_tokens": 400,
        "min_new_tokens": 50,
        "repetition_penalty": 1.1
    }

    # Create the model object
    try:
        model = Model(
            model_id=model_id,
            params=parameters,
            credentials=credentials,
            project_id=project_id
        )
    except Exception as e:
        return f"Error creating the AI model object. Details: {e}"


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
    
    # Generate the text
    try:
        generated_response = model.generate_text(prompt=prompt)
        return generated_response
    except Exception as e:
        # This will give us a much more specific error message if it fails.
        return f"Error during text generation: {e}"


# --- Section 3: Streamlit User Interface (Unchanged) ---
st.set_page_config(page_title="AI Travel Planner Chatbot", layout="centered")
st.title("🌍 AI Travel Planner Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Tell me about your dream trip..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🤖 Crafting your personalized journey..."):
            
            raw_response = generate_plan(prompt)

            # Check if the response is an error before trying to format it.
            if raw_response.strip().startswith("Error"):
                final_response = raw_response
            else:
                duration_match = re.search(r'(\d+)\s*day', prompt, re.IGNORECASE)
                duration = duration_match.group(1) if duration_match else None
                
                destination = None
                for city in df_destinations['City']:
                    if city.lower() in prompt.lower():
                        destination = city
                        break
                
                prefix = "Certainly, here is your travel plan:\n\n"
                if duration and destination:
                    prefix = f"Certainly, here is your {duration} day Travel Plan to {destination}:\n\n"
                elif duration:
                    prefix = f"Certainly, here is your {duration} day travel plan:\n\n"
                elif destination:
                    prefix = f"Certainly, here is your travel plan to {destination}:\n\n"

                day_plans = raw_response.split("Day ")
                day_plans = [plan for plan in day_plans if plan and plan.strip()]
                
                if len(day_plans) > 0 and any(char.isdigit() for char in day_plans[0]):
                    formatted_list = [f"- Day {plan.strip()}" for plan in day_plans]
                    formatted_itinerary = "\n".join(formatted_list)
                else:
                    formatted_itinerary = raw_response

                final_response = prefix + formatted_itinerary
            
            st.markdown(final_response)
    
    st.session_state.messages.append({"role": "assistant", "content": final_response})
