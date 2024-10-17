# TorRequestsWrapper

A Python wrapper for making HTTP requests through the Tor network, providing easy IP address anonymization and proxy functionality.

## Features

- Simple decorator for automatic Tor routing
- Support for GET, POST, PUT, and DELETE requests
- Automatic Tor connection verification
- IP address change confirmation
- Multiple Tor ports support (Browser and Service)

## Requirements

- Python 3.6+
- Tor Browser or Tor service installed and running
- Required Python packages:
  ```bash
  pip install requests requests[socks]
  ```

## Installation

1. Install the required Python packages:

   ```bash
   pip install requests requests[socks]
   ```

2. Ensure you have either:

   - Tor Browser running (default port: 9150)
   - OR Tor service running (default port: 9050)

3. Copy the `tor_requests.py` file to your project.

## Basic Usage

### 1. Using the Decorator (Recommended)

```python
from tor_requests import tor_request

@tor_request
def fetch_webpage(tor, url):
    response = tor.get(url)
    return response.text

# Use the function
content = fetch_webpage("https://example.com")
print(content)
```

### 2. Direct Class Usage

```python
from tor_requests import TorRequestsWrapper

# Create instance
tor = TorRequestsWrapper()

# Check and establish Tor connection
if tor.check_tor_connection():
    # Make requests
    response = tor.get("https://example.com")
    print(response.text)

    # POST request with data
    data = {"key": "value"}
    response = tor.post("https://example.com/api", json=data)
    print(response.json())
```

## Advanced Usage

### Custom Tor Ports

```python
# Specify custom Tor ports
tor = TorRequestsWrapper(tor_ports=[9050, 9150, 9051])
```

### Custom Timeout

```python
# Set custom timeout (in seconds)
tor = TorRequestsWrapper(timeout=20)
```

### All Available Methods

```python
# GET request
response = tor.get("https://example.com")

# POST request
response = tor.post("https://example.com", json={"key": "value"})

# PUT request
response = tor.put("https://example.com/resource", data={"key": "value"})

# DELETE request
response = tor.delete("https://example.com/resource")
```

## Error Handling

The wrapper includes built-in error handling for:

- Connection failures
- Tor service unavailability
- Request timeouts
- General HTTP errors

Example with error handling:

```python
try:
    tor = TorRequestsWrapper()
    if tor.check_tor_connection():
        response = tor.get("https://example.com")
        print(response.text)
except Exception as e:
    print(f"Error occurred: {e}")
```

## Important Notes

1. Always ensure your Tor service is running before making requests
2. The wrapper will automatically verify your IP has changed through Tor
3. Default timeout is 10 seconds but can be customized
4. All standard `requests` library parameters are supported

## Legal Considerations

- Ensure Tor usage is legal in your jurisdiction
- Respect website terms of service and robots.txt
- Be aware of potential security implications

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
