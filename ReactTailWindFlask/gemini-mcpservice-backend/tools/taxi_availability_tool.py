# server/tools/taxi_availability_tool.py
import requests

def get_taxi_availability(date_time: str = None) -> dict:
    """
    Fetches locations of available taxis in Singapore as GeoJSON from data.gov.sg.

    This function retrieves taxi availability data.
    - Data is retrieved every 30 seconds from LTA's Datamall.
    - The response is a valid GeoJSON object.
    - The timestamp in the response is the scrape time (LTA provides no other metadata).
    - The `date_time` parameter (YYYY-MM-DDTHH:mm:ss SGT) can be used to retrieve the latest
      available data at that moment in time.
    - It's recommended to call this endpoint about every minute.
    """
    base_url = "https://api.data.gov.sg/v1/transport/taxi-availability"
    params = {}
    if date_time:
        params["date_time"] = date_time

    tool_call_msg = f"TOOL SERVER: Called get_taxi_availability"
    if date_time:
        tool_call_msg += f" for date_time: {date_time}"
    else:
        tool_call_msg += " for latest data."
    print(tool_call_msg)

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        
        # GeoJSON is a specific format of JSON, so response.json() should work.
        data = response.json() 
        
        taxi_count = 0
        if "features" in data and data["features"] and "properties" in data["features"][0] and "taxi_count" in data["features"][0]["properties"]:
            taxi_count = data["features"][0]["properties"]["taxi_count"]
            
        print(f"TOOL SERVER: Successfully retrieved GeoJSON data. Found {taxi_count} taxis.")
        # print(f"TOOL SERVER: Responding with GeoJSON: {data}") # Potentially very verbose
        return data
    except requests.exceptions.HTTPError as http_err:
        error_message = f"HTTP error occurred: {http_err} - {response.text if response else 'No response body'}"
        print(f"TOOL SERVER: {error_message}")
        return {"error": "HTTPError", "message": str(http_err), "details": response.text if response else "No response body"}
    except requests.exceptions.RequestException as req_err:
        error_message = f"Request error occurred: {req_err}"
        print(f"TOOL SERVER: {error_message}")
        return {"error": "RequestException", "message": str(req_err)}
    except ValueError as json_err: # Includes JSONDecodeError, as GeoJSON is valid JSON
        error_message = f"JSON/GeoJSON decoding error: {json_err}"
        print(f"TOOL SERVER: {error_message}")
        return {"error": "JSONDecodeError", "message": "Failed to parse GeoJSON response from API."}