# import requests
# import zstandard as zstd

# # Send the GET request to the server
# url = "https://fle-rvd0i9o8-moo.com/ptsd/aax0ininm61n?referer=asianmilfhub.com"
# headers = {
# #'accept-encoding':'gzip, deflate, br, zstd',
# #'cookie':'file_id=35498330; aff=51778; ref_url=asianmilfhub.com; lang=1',
# 'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
# 'accept-language':'en-US,en;q=0.9'
# }
# response = requests.get(url,headers=headers)
# #print(response.headers)
# print(response.content)
# # Check the 'Content-Encoding' header to confirm it's zstd
# if 'zstd' in response.headers.get('Content-Encoding', ''):
#     # Decompress the Zstd-encoded content
#     dctx = zstd.ZstdDecompressor()
#     decompressed_data = dctx.decompress(response.content)

#     # You can now process the decompressed data as you would with a regular response
#     # For example, if it's JSON, you can load it into a Python object
#     import json
#     data = json.loads(decompressed_data)
#     print(data)
# else:
#     print("No Zstd encoding detected.")


# import requests

# def get_public_ip():
#     response = requests.get("https://httpbin.org/ip")
#     ip_data = response.json()
#     print(f"Public IP Address: {ip_data['origin']}")

# get_public_ip()


from urllib.parse import quote

url = "https://video-cf.xhcdn.com/%2BZQhUF2GmOwjFmcRTsbR3JPP6k3Np1HnTQKXaRX%2BCes%3D/104/1734876000/media=hls4/multi=256x144:144p:,426x240:240p:,854x480:480p:,1280x720:720p:,1920x1080:1080p:/025/109/406/720p.av1.mp4.m3u8"
encoded_url = quote(url, safe=":/?")
print(encoded_url)  # Output: https://example.com/video?id=123%2C456
