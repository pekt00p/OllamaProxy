from flask import Flask, request, Response, jsonify
import requests
import json
import configparser

app = Flask(__name__)

# Load configuration from ollama.ini file
def load_config():
    config = configparser.ConfigParser()
    config_file = 'ollama.ini'
    config.read(config_file)
    return config

# Load mock tokens from JSON file
def load_tokens():
    try:
        with open('tokens.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"tokens.json not found. Plese create it")



# Verify if the token is valid
def verify_token(token):
    tokens_data = load_tokens()
    for t in tokens_data['tokens']:
        if t['token'] == token:
            return True
    return False

# Get Ollama server URL from configuration
def get_ollama_url():
    config = load_config()
    host = config.get('ollama', 'host')
    port = config.get('ollama', 'port')
    return f"http://{host}:{port}"

# Proxy route that requires authentication
@app.route('/<path:subpath>', methods=['GET', 'POST'])
def proxy(subpath):
    # Get the Authorization header
    auth_header = request.headers.get('Authorization')
    
    if not auth_header:
        return jsonify({"error": "Authorization header is required"}), 401
    
    # Extract token from Authorization header (assuming Bearer token format)
    if auth_header.startswith('Bearer '):
        token = auth_header[7:]  # Remove 'Bearer ' prefix
    else:
        return jsonify({"error": "Invalid authorization header format"}), 401
    
    # Verify token
    if not verify_token(token):
        return jsonify({"error": "Invalid token"}), 403
    
    # Forward the request to the Ollama server
    try:
        # Get the target Ollama server URL from configuration
        ollama_url = get_ollama_url()
        
        # Build the full URL for the Ollama server
        full_url = f"{ollama_url}/{subpath}"
        
        # Forward the request to Ollama server
        if request.method == 'GET':    
            response = requests.get(full_url, params=request.args)
        elif request.method == 'POST':
            response = requests.post(full_url, data=request.data, params=request.args)
        else:
            return jsonify({"error": "Method not allowed"}), 405
        
        # Return the response from Ollama server

        return Response(
            response.content,
            status=response.status_code
            #headers=dict(response.headers)
        )
        
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to connect to Ollama server: {str(e)}"}), 502

# Health check endpoint
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8181, debug=True)