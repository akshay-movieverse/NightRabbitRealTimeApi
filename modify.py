from mitmproxy import http

# Intercept requests
def request(flow: http.HTTPFlow) -> None:
    # Check the request URL
    if "https://httpbin.org/ip" in flow.request.pretty_url:
        # Log or modify the request if needed
        #flow.request.headers["User-Agent"] = "Custom-User-Agent"  # Example modification
        print(f"Intercepted request: {flow.request.pretty_url}")
