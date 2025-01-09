import requests
import sys
import re

def send_http_request(server_address, uri, headers):
  """
  Sends an HTTP GET request to the specified server.

  Args:
    server_address: The address of the server.
    uri: The URI of the resource to request.
    headers: A dictionary of HTTP headers.

  Returns:
    The response object from the server.
  """

  url = f"http://{server_address}{uri}"
  response = requests.get(url, headers=headers)
  return response

def is_valid_address(address):
  # Regular expression for validating an IP address
  ip_pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
  # Regular expression for validating a URI
  uri_pattern = re.compile(r"^(?:http|ftp)s?://"  # http:// or https://
                r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain...
                r"localhost|"  # localhost...
                r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|"  # ...or ipv4
                r"\[?[A-F0-9]*:[A-F0-9:]+\]?)"  # ...or ipv6
                r"(?::\d+)?", re.IGNORECASE)  # optional port

  return ip_pattern.match(address) or uri_pattern.match(address)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_ml.py <server_address>")
        sys.exit(1)

    server_address = sys.argv[1]
    if not is_valid_address(server_address):
      print("Invalid server address. Must be a valid IP address or URI.")
      sys.exit(1)

    # Define the headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        "Referer": "https://34.247.173.104:31634/apps/auth/login",
        "auth_status": "NO-AUTH",
        "Host": "34.247.173.104",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "fr,fr-FR;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,fr-CH;q=0.5,de-DE;q=0.4,de;q=0.3",
        "bytes_sent": "29478",
        "body_bytes_sent": "29209",
        "Connection": "6592",
        "Connection-Requests": "2",
        "Sent-Http-Connection": "close",
        "Sent-Http-Content-Length": "29209",
        "Sent-Http-Content-Type": "image/png",
        "Sent-Http-Last-Modified": "Fri, 08 Nov 2024 07:16:19 GMT",
    }
    uri = '/auth/login'
    response = send_http_request(server_address, uri, headers)

    if response.status_code == 200:
        print("Request successful!")
        # Do something with the response data (e.g., save the image)
    else:
        print(f"Request failed with status code: {response.status_code}")

