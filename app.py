from flask import Flask, jsonify
import requests

app = Flask(__name__)

API_KEY = "AIzaSyDo_VD7jbFlapndIvIdpwYHuwn4yf-QAL8"  # Replace with your API key
CHANNEL_HANDLE = "@tsn"  # YouTube channel handle

def get_live_stream_content_id(api_key, channel_handle):
    base_url = "https://www.googleapis.com/youtube/v3/"

    # Step 1: Get the Channel ID from the Handle
    channel_response = requests.get(
        f"{base_url}search?part=snippet&type=channel&q={channel_handle}&key={api_key}"
    )
    
    if channel_response.status_code != 200:
        return {"error": "Error fetching channel data", "details": channel_response.json()}

    channel_data = channel_response.json()
    if not channel_data.get("items"):
        return {"error": "No channel found for handle."}

    channel_id = channel_data["items"][0]["id"]["channelId"]

    # Step 2: Fetch Videos from the Channel ID
    search_response = requests.get(
        f"{base_url}search?part=snippet&channelId={channel_id}&eventType=live&type=video&key={api_key}"
    )

    if search_response.status_code != 200:
        return {"error": "Error fetching live video data", "details": search_response.json()}

    live_data = search_response.json()
    if not live_data.get("items"):
        return {"error": "No ongoing live streams found for this channel."}

    # Step 3: Extract the Content ID
    content_id = live_data["items"][0]["id"]["videoId"]
    return {"content_id": content_id}

@app.route("/get_live_stream", methods=["GET"])
def fetch_live_stream():
    result = get_live_stream_content_id(API_KEY, CHANNEL_HANDLE)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
