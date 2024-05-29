from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import time

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.handle_index()
        elif self.path == '/simulate-error':
            self.handle_simulate_error()
        else:
            self.send_error(404, "Not Found")

    def handle_index(self):
        simulate_error = os.getenv("SIMULATE_ERROR")
        if simulate_error is None:
            response = {'status': 'OK'}
            self.send_response(200)
        else:
            response = {'status': 'error'}
            self.send_response(500)
        
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

    def handle_simulate_error(self):
        simulate_error = os.getenv("SIMULATE_ERROR")
        if simulate_error == "true":
            time.sleep(5)
            response = {'error': 'Erro simulado'}
            self.send_response(500)
        else:
            response = {'status': 'OK'}
            self.send_response(200)
        
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=3000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
