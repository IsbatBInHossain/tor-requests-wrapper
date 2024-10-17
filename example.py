# Usage Examples:
from tor_requests import TorRequestsWrapper, tor_request

# Example 1: Using the decorator
@tor_request
def fetch_webpage(tor, url):
    response = tor.get(url)
    return response.text

# Example 2: Direct class usage
def main():
    try:
        # Using decorator approach
        print("Example 1: Using decorator")
        content = fetch_webpage("https://example.com")
        print(content[:100])  # Print first 100 characters
        
        # Direct class usage
        print("\nExample 2: Direct class usage")
        tor = TorRequestsWrapper()
        if tor.check_tor_connection():
            response = tor.get("https://example.com")
            print(response.text[:100])
            
            # POST request example
            data = {"key": "value"}
            response = tor.post("https://example.com/api", json=data)
            print(response.status_code)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()