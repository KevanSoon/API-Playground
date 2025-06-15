# server/tool_definitions.py
from google.generativeai.types import FunctionDeclaration, Tool

# Define the schema for our demo tool
get_current_weather_func = FunctionDeclaration(
    name="get_current_weather",
    description=(
        "Retrieves the current weather conditions for a specified location. "
        "This tool can provide temperatures in either Celsius or Fahrenheit. "
        "If no unit is specified, Celsius is used by default."
    ),
    parameters={
        "type": "OBJECT",
        "properties": {
            "location": {
                "type": "STRING",
                "description": (
                    "The city name, or city and state/country, for which to fetch the weather. "
                    "Examples: 'London, UK', 'Tokyo', 'New York City'."
                )
            },
            "unit": {
                "type": "STRING",
                "description": (
                    "The desired temperature unit. Accepts 'celsius' or 'fahrenheit'. "
                    "Defaults to 'celsius' if not specified by the user or in the query."
                ),
                "enum": ["celsius", "fahrenheit"]
            }
        },
        "required": ["location"]
    }
)

# Define the schema for web search tool
web_search_func = FunctionDeclaration(
    name="perform_web_search",
    description=(
        "Performs a web search based on a given query string. "
        "The tool retrieves a list of search result titles and summaries. "
        "You can specify the maximum number of results to return."
    ),
    parameters={
        "type": "OBJECT",
        "properties": {
            "query": {
                "type": "STRING",
                "description": (
                    "The search query string to use for the web search. "
                    "Example: 'current events in technology', 'Python tutorials', 'latest weather news', 'General Election 2025 in Singapore','Pokemon','Kevan Soon SMU','Zulfaqar Hafez SIT'."
                )
            },
            "max_results": {
                "type": "INTEGER",
                "description": (
                    "Optional. The maximum number of search results to retrieve. "
                    "Defaults to 5 if not specified."
                ),
                
            }
        },
        "required": ["query"]
    }
)

# Define the schema for the carpark availability tool
get_carpark_availability_func = FunctionDeclaration(
    name="get_carpark_availability",
    description=(
        "Retrieves carpark availability data for Singapore from data.gov.sg. "
        "Data is updated approximately every minute. This tool can fetch the most current data "
        "or data for a specific past date and time if provided."
    ),
    parameters={
        "type": "OBJECT",
        "properties": {
            "date_time": {
                "type": "STRING",
                "description": (
                    "Optional. The specific date and time for which to fetch carpark availability. "
                    "Must be in 'YYYY-MM-DDTHH:mm:ss' format (Singapore Standard Time, SGT). "
                    "Example: '2023-10-26T10:30:00'. "
                    "If omitted, the API returns the latest available data."
                )
            }
        },
        "required": [] # date_time is optional as per the OpenAPI schema (required: false)
    }
)

# Define the schema for the traffic images tool
get_traffic_images_func = FunctionDeclaration(
    name="get_traffic_images",
    description=(
        "Retrieves the latest images from traffic cameras across Singapore. "
        "Data is sourced from LTA's Datamall and updated approximately every 20 seconds. "
        "Locations of the cameras are provided in the response. "
        "Use the optional 'date_time' parameter to fetch images for a specific moment in time; "
        "otherwise, the most current images are returned."
    ),
    parameters={
        "type": "OBJECT",
        "properties": {
            "date_time": {
                "type": "STRING",
                "description": (
                    "Optional. The specific date and time for which to fetch traffic images. "
                    "Must be in 'YYYY-MM-DDTHH:mm:ss' format (Singapore Standard Time, SGT). "
                    "Example: '2023-10-27T14:00:00'. "
                    "If omitted, the API returns the latest available image data."
                )
            }
        },
        "required": [] # date_time is optional as per the OpenAPI schema (required: false)
    }
)

# Define the schema for the taxi availability tool
get_taxi_availability_func = FunctionDeclaration(
    name="get_taxi_availability",
    description=(
        "Retrieves the locations of available taxis in Singapore as GeoJSON data. "
        "Data is sourced from LTA's Datamall and updated approximately every 30 seconds. "
        "The response is a valid GeoJSON object suitable for mapping tools. "
        "Use the optional 'date_time' parameter to fetch data for a specific moment in time; "
        "otherwise, the most current data is returned. The timestamp in the response indicates the scrape time."
    ),
    parameters={
        "type": "OBJECT",
        "properties": {
            "date_time": {
                "type": "STRING",
                "description": (
                    "Optional. The specific date and time for which to fetch taxi availability. "
                    "Must be in 'YYYY-MM-DDTHH:mm:ss' format (Singapore Standard Time, SGT). "
                    "Example: '2023-10-28T09:15:00'. "
                    "If omitted, the API returns the latest available data."
                )
            }
        },
        "required": [] # date_time is optional as per the OpenAPI schema (required: false)
    }
)

# Define the schema for the deepsearcher tool
get_deepsearcher_func = FunctionDeclaration(
    name="get_deepsearcher",
    description=(
        "Performs a deep semantic search for information across any specified context or content. "
        "This tool allows querying structured or unstructured data using natural language. "
        "The content to be searched can be text, documents, webpages, datasets, or any other "
        "relevant source. The system dynamically loads and indexes the target content before executing the query."
    ),
    parameters={
        "type": "OBJECT",
        "properties": {
            "search_info": {
                "type": "STRING",
                "description": (
                    "The natural language query or search question to use when finding relevant information."
                )
            },
        },
        "required": ["search_info"]
    }
)


# Create a Tool object that contains our function declaration
WEATHER_TOOL = Tool(function_declarations=[get_current_weather_func])
WEB_SEARCH_TOOL = Tool(function_declarations=[web_search_func])
CARPARK_AVAILABILITY_TOOL = Tool(function_declarations=[get_carpark_availability_func])
TRAFFIC_IMAGES_TOOL = Tool(function_declarations=[get_traffic_images_func])
TAXI_AVAILABILITY_TOOL = Tool(function_declarations=[get_taxi_availability_func])
DEEPSEARCHER_TOOL = Tool(function_declarations=[get_deepsearcher_func])

# For the server to know which function to call (not directly used by Gemini in this client)
AVAILABLE_TOOLS_GEMINI_SCHEMA = {
    "get_current_weather": get_current_weather_func,
    "perform_web_search": web_search_func,
    "get_carpark_availability": get_carpark_availability_func,
    "get_traffic_images": get_traffic_images_func,
    "get_taxi_availability": get_taxi_availability_func,
    "get_deepsearcher": get_deepsearcher_func,
}