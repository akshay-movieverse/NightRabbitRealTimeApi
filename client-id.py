import re
import requests
from flask import Flask, request, jsonify, Response

app = Flask(__name__)

# Example video service URL (replace with the actual URL for video token retrieval)
VIDEO_SERVICE_URL = 'https://fle-rvd0i9o8-moo.com/ptsd/nbvxf8fy3nft?referer=asianmilfhub.com'


def main_keys(ht):

    # Step 2: Use regular expression to find the script content containing the eval function
    script_content = None
    match = re.search(r'<script[^>]*data-cfasync=\'false\'[^>]*>(.*?)</script>', ht, re.DOTALL)

    if match:
        script_content = match.group(1)  # Extract the content inside the <script> tag
        print("Script Content Found:")
        print(script_content[:200])  # Print first 200 characters for review

    # Step 3: Extract the dynamic token and ID from the script content
    if script_content:
        # Extract the token (a string of letters, digits, and underscores)
        token_match = re.search(r"([a-zA-Z0-9_]{32,})", script_content)
        if token_match:
            token = token_match.group(0)
            print(f"Extracted Token: {token}")

        # Extract the ID (a 10-digit number)
        id_match = re.search(r"\d{10}", script_content)
        if id_match:
            id_value = id_match.group(0)
            print(f"Extracted ID: {id_value}")

    else:
        print("No script with the specified attribute found.")

@app.route('/video')
def proxy_video():
    # Retrieve the client’s IP address (this will be forwarded to the video service)
    client_ip = request.headers.get("X-Forwarded-For", "").split(",")[0].strip() or request.remote_addr
    
    print(client_ip)
    
    # Prepare the headers (You can include additional headers if needed, like user-agent or cookies)
    headers = {
        
        'X-Forwarded-For': client_ip,  # Send the client's IP to the video service
        "Connection": "close",
        #'Accept': 'application/json'    # Assuming the response is in JSON format
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'accept-language':'en-US,en;q=0.9',
        'sec-fetch-dest':'iframe',
        'X-Real-IP':client_ip
    }
    # proxies = {
    #     "http": "http://127.0.0.1:8080",  # mitmproxy runs on this port
    #     "https": "http://127.0.0.1:8080",
    # }
    # Proxy the request to the actual video service (this could be token generation or video fetching)
    try:
        response = requests.get(VIDEO_SERVICE_URL, headers=headers, params=request.args)
        # response = requests.get("https://httpbin.org/ip", headers=headers)
        # ip_data = response.json()
        # print(f"Public IP Address: {ip_data['origin']}")
        # print(response.request.headers)
        # print("Outgoing headers:", headers)
        #print(response)
        # Check if the response from the video service is successful
        if response.status_code == 200:
            # Return the video URL and token (or any other data)
            #print(response.text)
            main_keys(response.text)
            return jsonify(response.text)

        else:
            return jsonify({"error": "Failed to fetch video token"}), 500

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


# Function to stream the .ts file from the external URL
# @app.route('/stream/<path:filename>')
# def stream_ts(filename):
#     # External URL for the .ts file
#     external_url = f"https://be6721.rcr72.waw04.cdn255.com/hls2/06/06171/uzx8thpyd4um_x/{filename}?t=xymxiTdMa1ifgLb_xPSBKYLpskMXjIzR7RwD7YtpWXQ&s=1733654980&e=10800&f=30858490&srv=53&asn=9829&sp=5500&p="

#     # You can dynamically modify the URL if needed based on the filename or parameters
#     # For example, if you want to use the `filename` as part of the query string or path:
#     # external_url = f"https://example.com/{filename}"

#     # Send a GET request to the external server to fetch the .ts file
#     response = requests.get(external_url, stream=True)

#     if response.status_code == 200:
#         # Return the external file as a stream to the client
#         return Response(response.iter_content(chunk_size=1024), content_type="video/mp2t")
#     else:
#         # If the external file isn't found, return a 404 error
#         return "File not found", 404


if __name__ == '__main__':
    app.run(host='192.168.1.47', port=5000,debug=True)
