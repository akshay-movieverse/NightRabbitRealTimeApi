import os
import re
from flask import Flask, Response, render_template, request, jsonify, url_for
import requests
from bs4 import BeautifulSoup
import urllib
from waitress import serve

app = Flask(__name__)


def getQulaity(url):
    # Regular expression to match the multi parameter and its values
    pattern = r"multi=([a-zA-Z0-9:,=]+)"

    # Search for the pattern in the URL
    match = re.search(pattern, url)

    if match:
        # Extract the value of multi
        multi_value = match.group(1)
        
        # Split the multi values (separated by commas) into a list
        quality_values = multi_value.split(',')
        
        # Extract only the resolution (e.g., 144p, 240p) part from each quality value
        resolutions = [re.search(r'(\d+p)', quality).group(1) for quality in quality_values if re.search(r'(\d+p)', quality)]
        
        # Output the extracted resolutions
        #print(resolutions)
        return resolutions
    else:
        return None
        #print("No 'multi' parameter found.")


# Helper function to generate the master.m3u8 content
# def generate_master_m3u8(url):
#     # Regular expression to match the multi parameter and its values
#     pattern = r"multi=([a-zA-Z0-9:,=]+)"
    
#     # Search for the pattern in the URL
#     match = re.search(pattern, url)
    
#     if match:
#         # Extract the value of multi
#         multi_value = match.group(1)
        
#         # Split the multi values (separated by commas) into a list
#         quality_values = multi_value.split(',')
        
#         # Extract only the resolution (e.g., 144p, 240p) part from each quality value
#         resolutions = [re.search(r'(\d+p)', quality).group(1) for quality in quality_values if re.search(r'(\d+p)', quality)]
        
#         # Base URL part to create the m3u8 file (assuming the URL remains constant for each resolution)
#         #base_url = "https://video-cf.xhcdn.com/43h3xnOLuBGDcSFDbJDoDgzVtpW9xbiFOp5A4278yGg%3D/121/1733572800/media=hls4/"
        
#         # Generate the master.m3u8 content
#         m3u8_content = "#EXTM3U\n"
#         for resolution in resolutions:
#             # Generate the media playlist URL for each resolution
#             m3u8_content += f"#EXT-X-STREAM-INF:BANDWIDTH=500000,RESOLUTION={resolution}\n"
#             m3u8_content += f"{url.replace('_TPL_',resolution)}\n"
        
#         return m3u8_content
#     else:
#         return None
def everyUrl(video_link,qulaity):
    final_list= []
    for resolution in qulaity:
        final_list.append({'link': video_link.replace('_TPL_',resolution), 'resolution': resolution})
        #print(resolution)
    return final_list
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.json.get('url')
    try:
        # Scrape the page content
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Example of extracting a link (customize this part)
        video_link = None
        # Step 3: Find the first <link> tag with rel="preload"
        preload_link = soup.find('link', rel='preload')

        # Step 4: Check if the link contains .m3u8 and _TPL_
        if preload_link:
            href = preload_link.get('href', '')
            video_link = href
        #print(video_link)
        #master_data = generate_master_m3u8(href)
            # Use urllib.parse.quote to ensure href is properly encoded for URL query parameters
        # encoded_href = urllib.parse.quote(video_link)
        # master_url = url_for('serve_master_m3u8', href=encoded_href, _external=True)
        master_url = everyUrl(video_link,getQulaity(video_link))
        print(master_url)
        if video_link:
            
            return jsonify({'success': True, 'video_data': master_url})
        else:
            return jsonify({'success': False, 'message': 'No video link found'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    #serve(app, host='192.168.1.47', port=5000, threads=4)
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)
