# Ollama Proxy Server

A minimal Flask proxy server that forwards requests to a local Ollama server with token-based authentication.

## Features

- Token-based authentication for API access
- Forwarding of all HTTP methods (GET, POST) to local Ollama server
- Health check endpoint
- Mock tokens included in `tokens.json`
- External config file `ollama.ini`

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the proxy server:
   ```bash
   python app.py
   ```

3. The proxy will be available at `http://localhost:8181`

## Usage

To access the Ollama server through the proxy, include a valid token in the Authorization header:

```bash
curl -H "Authorization: Bearer token_12345" http://localhost:8181/api/generate
```

## Tokens

Tokens are available in `tokens.json`:



## Endpoints

- `GET /health` - Health check endpoint
- All other endpoints are proxied to `http://localhost:11434` (default Ollama server)

## Configuration

The proxy uses an external configuration file `ollama.ini` to specify the Ollama server address and port.

Example configuration:
```ini
[ollama]
host = localhost
port = 11434
```


The proxy assumes the local Ollama server is running at `http://localhost:11434`. If your Ollama server runs on a different port or address, modify the `ollama.ini` file accordingly.