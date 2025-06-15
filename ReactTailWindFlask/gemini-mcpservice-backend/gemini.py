from flask import Flask, request, jsonify
from flask_cors import CORS
# client/gemini_api_client.py
import os
import json
import requests # For calling the tool server
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from dotenv import load_dotenv
# Import the tool definition from the server directory (adjust path as needed)
# This assumes client and server are siblings in the project structure
import sys
from tools.tool_definitions import WEATHER_TOOL, WEB_SEARCH_TOOL,CARPARK_AVAILABILITY_TOOL,TAXI_AVAILABILITY_TOOL,TRAFFIC_IMAGES_TOOL,DEEPSEARCHER_TOOL
from tools.weather_tool import get_current_weather
from tools.websearch_tool import perform_web_search
from tools.carkpark_availability_tool import get_carpark_availability
from tools.taxi_availability_tool import get_taxi_availability
from tools.traffic_images_tool import get_traffic_images
from tools.deepsearcher_tool import get_deepsearcher
from supabase import create_client, Client


app = Flask(__name__)
CORS(app)

# Map tool names to their actual functions
TOOL_EXECUTORS = {
    "get_current_weather": get_current_weather,
    "perform_web_search": perform_web_search,
    "get_carpark_availability": get_carpark_availability,
    "get_taxi_availability": get_taxi_availability,
    "get_traffic_images": get_traffic_images,
    "get_deepsearcher": get_deepsearcher
}

sys.path.append(os.path.join(os.path.dirname(__file__), '..')) # Add project root to sys.path

# from server.tool_definitions import WEATHER_TOOL # Our defined tool schema for Gemini

# Load environment variables from .env in the project root
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")


genai.configure(api_key=GEMINI_API_KEY)

# --- Gemini Model Configuration ---
generation_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}
safety_settings = [
    {"category": HarmCategory.HARM_CATEGORY_HARASSMENT, "threshold": HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE},
    {"category": HarmCategory.HARM_CATEGORY_HATE_SPEECH, "threshold": HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE},
    {"category": HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT, "threshold": HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE},
    {"category": HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, "threshold": HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE},
]

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash", # or "gemini-1.0-pro"
    generation_config=generation_config,
    safety_settings=safety_settings,
    tools=[WEATHER_TOOL,WEB_SEARCH_TOOL,CARPARK_AVAILABILITY_TOOL,TRAFFIC_IMAGES_TOOL,TAXI_AVAILABILITY_TOOL,DEEPSEARCHER_TOOL] # Pass the tool schema here
)

def execute_tool(tool_name, tool_args):
    tool_name = tool_name
    args = tool_args

    print(f"TOOL SERVER: Received request to execute tool: {tool_name} with args: {args}")

    if tool_name in TOOL_EXECUTORS:
        try:
            executor = TOOL_EXECUTORS[tool_name]
            result = executor(**args)
            return {"result": result}  # ✅ Return plain dict, not jsonify
        except Exception as e:
            print(f"TOOL SERVER: Error executing tool {tool_name}: {e}")
            return {"error": f"Error executing tool {tool_name}: {str(e)}"}
    else:
        print(f"TOOL SERVER: Tool '{tool_name}' not found.")
        return {"error": f"Tool '{tool_name}' not found"}



def run_conversation_with_tools(user_prompt: str):
    print(f"\n👤 User: {user_prompt}")
    
    # Initial message to Gemini
    # When using tools, it's often better to manage history explicitly
    # for complex conversations. For a single turn, this is simpler.
    chat = model.start_chat(history=[]) # Start a new chat session for each run_conversation for simplicity
    
    response = chat.send_message(user_prompt)
    
    # Loop to handle potential multiple tool calls (though less common in simple queries)
    while response.candidates[0].content.parts[0].function_call.name:
        function_call_part = response.candidates[0].content.parts[0]
        tool_name = function_call_part.function_call.name
        tool_args = {key: value for key, value in function_call_part.function_call.args.items()}

        print(f"🛠️ Gemini wants to call tool: {tool_name} with arguments: {tool_args}")

        # Call our MCP tool server
        # api_response = call_tool_server(tool_name, tool_args)
        api_response = execute_tool(tool_name,tool_args)

        # Send the tool's response back to Gemini
        # Note: The 'name' here must match the 'name' in the FunctionCall

        # Construct the function response payload manually as a dictionary.
        # This structure mimics what Part.from_function_response would create,
        # and send_message can accept PartDict-like dictionaries.
        manual_function_response_part = {
            "function_response": {
                "name": tool_name,
                "response": { # This inner dict is the 'Struct' payload for Gemini.
                              # The 'content' key here is a convention to pass the tool's
                              # actual result (api_response) to the model.
                    "content": api_response
                }
            }
        }
        
        print(f"↪️ GEMINI CLIENT: Sending tool response (manual dict) to Gemini: {manual_function_response_part}")
        
        # Send the function response back to the model.
        response = chat.send_message(
            [manual_function_response_part] 
        )
        # Check if Gemini wants to call another tool or gives a final answer
        if not response.candidates[0].content.parts[0].function_call.name:
            break # Exit loop if no more function calls

    # Print the final response from Gemini
    if response.candidates and response.candidates[0].content.parts:
        final_text = "".join(part.text for part in response.candidates[0].content.parts if hasattr(part, 'text'))
        print(f"\n✨ Gemini: {final_text}")

        url: str = os.environ.get("SUPABASE_URL")
        key: str = os.environ.get("SUPABASE_KEY")
        supabase: Client = create_client(url, key)

        # ✅ Store user prompt in Supabase
        prompt_insert = supabase.table("user_prompts").insert({
            "prompt_text": user_prompt
        }).execute()

        # Get the inserted prompt's ID
        prompt_id = prompt_insert.data[0]['id']

        # ✅ Store Gemini response in Supabase
        supabase.table("chatbot_responses").insert({
            "prompt_id": prompt_id,
            "response_text": final_text
        }).execute()

        return final_text
    else:
        print("\n✨ Gemini: (No text content in final response)")
        print(f"Full response object: {response}")
        


@app.route('/gemini-response', methods=['POST'])
def get_response():
    data = request.get_json()
    user_prompt = data.get("text")  # Updated to match the frontend's JSON key
    print("Received prompt from frontend:", user_prompt)
    response = run_conversation_with_tools(user_prompt)
    print(response)
    return jsonify({"result": response})



@app.route("/chartdata")
def read_chart():
    data = [
         {"name": "T2-R2AW1", "Median": 40, "Minimum": 40},
         {"name": "T2-R1AW2", "Median": 39.31, "Minimum": 39.31},
         {"name": "T1-R1AW1", "Median": 39.23, "Minimum": 12.59},
         {"name": "T1-R1W1", "Median": 38.89, "Minimum": 35.05},

    ]
    return {"chart_data": data}

@app.route("/denguecluster")
def get_api():      
    dataset_id = "d_dbfabf16158d1b0e1c420627c0819168"
    url = f"https://api-open.data.gov.sg/v1/public/api/datasets/{dataset_id}/poll-download"

    response = requests.get(url)
    json_data = response.json()

    

    if json_data['code'] != 0:
        return jsonify({"error": json_data['errMsg']}), 500

    # This URL contains the actual GeoJSON
    geojson_url = json_data['data']['url']
    geojson_response = requests.get(geojson_url)
    print(geojson_response)

    # Parse GeoJSON content and return it
    try:
        geojson_data = geojson_response.json()
        return jsonify(geojson_data)
    except ValueError:
        return jsonify({"error": "Invalid GeoJSON response"}), 500

@app.route("/rainfallstations")
def rainfall_geojson():
    # Data.gov.sg rainfall API
    api_url = "https://api.data.gov.sg/v1/environment/rainfall"
    response = requests.get(api_url)
    json_data = response.json()

    # Extract stations and rainfall readings
    stations = json_data["metadata"]["stations"]
    readings = json_data["items"][0]["readings"]
    reading_map = {r["station_id"]: r["value"] for r in readings}

    print(json_data)

    geojson = {
        "type": "FeatureCollection",
        "features": []
    }

    for station in stations:
        station_id = station["id"]
        value = reading_map.get(station_id)

        # Optional: skip stations with no data
        if value is None:
            continue

        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [station["location"]["longitude"], station["location"]["latitude"]],
            },
            "properties": {
                "name": station["name"],
                "stationId": station_id,
                "rainfall_mm": value
            }
        }
        
        geojson["features"].append(feature)
        # geojson["features"].append({
        #         "type": "Feature",
        #         "geometry": {
        #             "type": "Point",
        #             "coordinates": [103.85, 1.29],  # Sample coords near Marina Bay
        #         },
        #         "properties": {
        #             "name": "Hardcoded Rain Station",
        #             "stationId": "HARDCODED_1",
        #             "rainfall_mm": 10.0
        #         }
        #     })

    
       

    return jsonify(geojson)

@app.route('/supabase-info')
def get_supabase_info():
    # Example static data
    data = {"data": "Hello"}
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    prompts_res = supabase.table("user_prompts").select("id, prompt_text, created_at").execute()
 

    # Fetch all chatbot responses
    responses_res = supabase.table("chatbot_responses").select("prompt_id, response_text, created_at").execute()


    prompts = prompts_res.data
    responses = responses_res.data

    print(responses)
    print(prompts)

    # Merge and sort by created_at
    combined = []

    # Add all prompts as entries with role=user
    for p in prompts:
        combined.append({
            "role": "user",
            "text": p["prompt_text"],
            "created_at": p["created_at"],
            "prompt_id": p["id"],
        })

    # Add all responses as entries with role=bot
    for r in responses:
        combined.append({
            "role": "bot",
            "text": r["response_text"],
            "created_at": r["created_at"],
            "prompt_id": r["prompt_id"],
        })

    # Sort combined by created_at ascending
    combined_sorted = sorted(combined, key=lambda x: x["created_at"])

    print("This is combined_sorted: " + str(combined_sorted))

    # Optional: you can group them by prompt-response pairs if you want

    return jsonify({"history": combined_sorted})


if __name__ == '__main__':
    app.run(debug=True)
