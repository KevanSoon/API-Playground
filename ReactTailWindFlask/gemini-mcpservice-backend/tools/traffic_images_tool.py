# server/tools/traffic_images_tool.py
import requests

def get_traffic_images(date_time: str = None) -> dict:
    """
    Fetches the latest images from traffic cameras in Singapore from data.gov.sg.

    This function retrieves traffic image data.
    - Data is sourced from LTA's Datamall and updated approximately every 20 seconds.
    - Camera locations are also provided in the response.
    - The `date_time` parameter (YYYY-MM-DDTHH:mm:ss SGT) can be used to retrieve the latest
      available data at that moment in time.
    - It's recommended to call this endpoint about every minute.
    """
    base_url = "https://api.data.gov.sg/v1/transport/traffic-images"
    params = {}
    if date_time:
        params["date_time"] = date_time

    tool_call_msg = f"TOOL SERVER: Called get_traffic_images"
    if date_time:
        tool_call_msg += f" for date_time: {date_time}"
    else:
        tool_call_msg += " for latest data."
    print(tool_call_msg)

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        
        data = response.json()
        items_count = 0
        if "items" in data and len(data["items"]) > 0 and "cameras" in data["items"][0]:
            items_count = len(data["items"][0]["cameras"])
        
        print(f"TOOL SERVER: Successfully retrieved data. Returning info for {items_count} cameras.")
        # print(f"TOOL SERVER: Responding with: {data}") # Potentially very verbose for image data
        return data
    except requests.exceptions.HTTPError as http_err:
        error_message = f"HTTP error occurred: {http_err} - {response.text if response else 'No response body'}"
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