# server/tools/carpark_availability_tool.py
import requests

def get_carpark_availability(date_time: str = None) -> dict:
    """
    Fetches carpark availability from the data.gov.sg API.

    This function retrieves carpark availability information.
    - Data is typically retrieved every minute.
    - The `date_time` parameter (YYYY-MM-DDTHH:mm:ss SGT) can be used to get data for a specific moment.
    - For detailed information about carparks, refer to: https://data.gov.sg/dataset/hdb-carpark-information
    """
    base_url = "https://api.data.gov.sg/v1/transport/carpark-availability"
    params = {}
    if date_time:
        params["date_time"] = date_time

    tool_call_msg = f"TOOL SERVER: Called get_carpark_availability"
    if date_time:
        tool_call_msg += f" for date_time: {date_time}"
    else:
        tool_call_msg += " for latest data."
    print(tool_call_msg)

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        
        data = response.json()
        print(f"TOOL SERVER: Successfully retrieved data. Returning {len(data.get('items', []))} items.")
        # print(f"TOOL SERVER: Responding with: {data}") # Potentially very verbose
        return data
    except requests.exceptions.HTTPError as http_err:
        error_message = f"HTTP error occurred: {http_err} - {response.text}"
        print(f"TOOL SERVER: {error_message}")
        return {"error": "HTTPError", "message": str(http_err), "details": response.text if response else "No response body"}
    except requests.exceptions.RequestException as req_err:
        error_message = f"Request error occurred: {req_err}"
        print(f"TOOL SERVER: {error_message}")
        return {"error": "RequestException", "message": str(req_err)}
    except ValueError as json_err: # Includes JSONDecodeError
        error_message = f"JSON decoding error: {json_err}"
        print(f"TOOL SERVER: {error_message}")
        return {"error": "JSONDecodeError", "message": "Failed to parse JSON response from API."}