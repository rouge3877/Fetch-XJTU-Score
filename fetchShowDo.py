import requests
import re
import time
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import sys

def fetch_show_do(cookies_file, xh):
    """
    Reads cookies from 'cookies_file', sends a GET request with parameter 'xh',
    and returns a tuple (True, HTML text) if successful, or (False, error message).
    """
    # Parse cookies file
    cookies = {}
    try:
        with open(cookies_file, 'r', encoding='utf-8') as f:
            cookie_line = f.read().strip()
    except Exception as e:
        return (False, f"Failed to read cookies file: {e}")
    
    if not cookie_line:
        return (False, "No cookies found in the file.")
    
    # Split cookie_line into key-value pairs
    for ck in cookie_line.split(';'):
        ck = ck.strip()
        if '=' in ck:
            key, value = ck.split('=', 1)
            cookies[key.strip()] = value.strip()
    
    # Set target URL and request parameters
    url = 'https://ehall.xjtu.edu.cn/jwapp/sys/frReport2/show.do'
    params = {
        'reportlet': 'bkdsglxjtu/XAJTDX_BDS_CJ.cpt',
        '__showtoolbar__': 'false',
        'xh': xh
    }
    
    # Set optional request headers (simulate browser)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/112.0.0.0 Safari/537.36",
        'Referer': 'https://ehall.xjtu.edu.cn/login',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive'
    }
    
    # Send request and handle response
    try:
        response = requests.get(url, params=params, cookies=cookies, headers=headers, timeout=10)
    except requests.exceptions.RequestException as e:
        return (False, f"GET request failed: {e}")
    
    # Check response and return result
    if response.status_code == 200:
        print("Successfully reached the target URL.")
        return (True, response.text)
    else:
        return (False, f"Request failed, status code: {response.status_code}")


if __name__ == "__main__":
    """
    Main function to read cookies, call fetch_show_do
    if -o <file> is specified, save the HTML content to a file.
    """

    # Check command line arguments
    if len(sys.argv) <= 2:
        print("Usage: python fetchShowDo.py [cookies_file_path] [xh_value]")
        sys.exit(1)

    # Parse command line arguments
    cookies_path = sys.argv[1]
    xh_value = sys.argv[2]

    # Call fetch_show_do function
    success, result = fetch_show_do(cookies_path, xh_value)

    if success:
        if len(sys.argv) > 3 and sys.argv[3] == '-o' and len(sys.argv) > 4:
            output_file = sys.argv[4]
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(result)
                print(f"Content saved as {output_file}")
            except Exception as e:
                print(f"Failed to save content: {e}")
                sys.exit(1)
        else:
            print(result)
    else:
        print(result)
        sys.exit(1)
