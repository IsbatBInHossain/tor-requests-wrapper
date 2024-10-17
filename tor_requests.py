"""
TorRequestsWrapper - A Python wrapper for making HTTP requests through Tor

This wrapper allows you to easily make HTTP requests through the Tor network,
providing IP address anonymization and proxy functionality.

Installation:
-------------
Required packages:
    pip install requests requests[socks]

You must also have Tor running on your system:
    - Either Tor Browser (default port 9150)
    - Or Tor service (default port 9050)

Basic Usage:
-----------
1. Simple decorator approach:

    from tor_requests import tor_request

    @tor_request
    def fetch_webpage(tor, url):
        response = tor.get(url)
        return response.text

    # Use the function
    content = fetch_webpage("https://example.com")
    print(content)

2. Direct class usage:

    from tor_requests import TorRequestsWrapper

    # Create instance
    tor = TorRequestsWrapper()
    
    # Check and establish Tor connection
    if tor.check_tor_connection():
        # Make requests
        response = tor.get("https://example.com")
        print(response.text)

Available HTTP Methods:
---------------------
- get(url, **kwargs)
- post(url, **kwargs)
- put(url, **kwargs)
- delete(url, **kwargs)

All methods support standard requests library kwargs.
"""

import requests
from functools import wraps
import socket

class TorRequestsWrapper:
    def __init__(self, tor_ports=[9150, 9050], timeout=10):
        """
        Initialize the TorRequestsWrapper.
        
        Args:
            tor_ports (list): List of ports to try for Tor connection. Default [9150, 9050]
            timeout (int): Request timeout in seconds. Default 10
        """
        self.tor_ports = tor_ports
        self.timeout = timeout
        self.ip_check_url = 'https://api.ipify.org?format=json'
        self.proxies = None
        
    def _create_proxies(self, port):
        return {
            'http': f'socks5h://127.0.0.1:{port}',
            'https': f'socks5h://127.0.0.1:{port}'
        }
        
    def check_tor_connection(self):
        """
        Verify Tor connection by comparing direct IP with Tor IP.
        
        Returns:
            bool: True if connected to Tor, False otherwise
        """
        direct_ip = self._get_direct_ip()
        if not direct_ip:
            print("Warning: Unable to get direct IP. Continuing with Tor check...")
        
        for port in self.tor_ports:
            try:
                self.proxies = self._create_proxies(port)
                tor_ip = self._get_tor_ip()
                if tor_ip and tor_ip != direct_ip:
                    print(f"Connected to Tor! Tor IP: {tor_ip}")
                    return True
            except requests.RequestException as e:
                print(f"Error checking Tor connection on port {port}: {e}")
            except socket.error as e:
                print(f"Socket error on port {port}: {e}")
        
        print("Tor connection failed. Unable to connect through any configured port.")
        return False
        
    def _get_direct_ip(self):
        try:
            response = requests.get(self.ip_check_url, timeout=self.timeout)
            return response.json()['ip']
        except requests.RequestException as e:
            print(f"Error getting direct IP: {e}")
            return None
            
    def _get_tor_ip(self):
        try:
            response = requests.get(self.ip_check_url, proxies=self.proxies, timeout=self.timeout)
            return response.json()['ip']
        except requests.RequestException as e:
            raise
            
    def _tor_request(self, method, *args, **kwargs):
        if not self.proxies:
            raise Exception("Tor proxy not configured. Run check_tor_connection() first.")
        kwargs['proxies'] = self.proxies
        return getattr(requests, method)(*args, **kwargs)
        
    def get(self, *args, **kwargs):
        """Make a GET request through Tor"""
        return self._tor_request('get', *args, **kwargs)
        
    def post(self, *args, **kwargs):
        """Make a POST request through Tor"""
        return self._tor_request('post', *args, **kwargs)
        
    def put(self, *args, **kwargs):
        """Make a PUT request through Tor"""
        return self._tor_request('put', *args, **kwargs)
        
    def delete(self, *args, **kwargs):
        """Make a DELETE request through Tor"""
        return self._tor_request('delete', *args, **kwargs)

def tor_request(func):
    """
    Decorator to automatically handle Tor connection for a function.
    The decorated function must accept 'tor' as its first argument after self (if in a class).
    
    Example:
        @tor_request
        def fetch_webpage(tor, url):
            response = tor.get(url)
            return response.text
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        tor = TorRequestsWrapper()
        if not tor.check_tor_connection():
            raise Exception("Tor connection failed. Make sure Tor is running and configured correctly.")
        return func(tor, *args, **kwargs)
    return wrapper


