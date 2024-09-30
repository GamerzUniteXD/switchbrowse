import http.server
import socketserver
import requests

PORT = 8080  # You can choose a different port if necessary

class Proxy(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Forward the request to the actual destination
        try:
            # Get the full URL from the request path
            url = self.path
            
            # Make a GET request to the destination URL
            response = requests.get(url)
            
            # Send the response code
            self.send_response(response.status_code)
            
            # Forward the headers
            for key, value in response.headers.items():
                self.send_header(key, value)
            self.end_headers()
            
            # Forward the content
            self.wfile.write(response.content)

        except Exception as e:
            self.send_error(500, f"Error: {e}")

    def do_POST(self):
        # Same as GET but with POST forwarding
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # Get the full URL from the request path
            url = self.path
            
            # Forward the POST request to the destination URL
            response = requests.post(url, data=post_data)
            
            # Send the response code
            self.send_response(response.status_code)
            
            # Forward the headers
            for key, value in response.headers.items():
                self.send_header(key, value)
            self.end_headers()
            
            # Forward the content
            self.wfile.write(response.content)

        except Exception as e:
            self.send_error(500, f"Error: {e}")

# Set up the proxy server
with socketserver.TCPServer(("", PORT), Proxy) as httpd:
    print(f"Serving proxy on port {PORT}")
    httpd.serve_forever()
