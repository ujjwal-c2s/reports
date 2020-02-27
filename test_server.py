import http.server
import socketserver
import os

PORT = 8000
data_dir = os.path.join(os.path.dirname(__file__), 'data')

Handler = http.server.SimpleHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler)

httpd.serve_forever()
