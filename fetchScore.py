import requests
import re
import time
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import sys

def fetch_score_page(cookies_file, html_content):
    """
    Retrieve the score page using the provided cookies file and HTML content.

    This function performs:
    1. Reading cookies from the specified file.
    2. Extracting the session ID from the given HTML content.
    3. Constructing the target URL with the extracted session ID.
    4. Sending a GET request to the URL using the cookies and headers.
    5. Returning the response text or an error message.
    """
    # 1. Read cookies from the specified file
    cookies = {}
    try:
        with open(cookies_file, 'r', encoding='utf-8') as f:
            cookie_line = f.read().strip()
    except Exception as e:
        return (False, f"Failed to read the cookies file: {e}")
    
    # Split the cookie_line by ';' and then by '=' to get key-value pairs
    for ck in cookie_line.split(';'):
        ck = ck.strip()
        if '=' in ck:
            key, value = ck.split('=', 1)
            cookies[key.strip()] = value.strip()
    
    # 2. Extract session ID from the given HTML content
    try:
        soup = BeautifulSoup(html_content, 'html.parser')  # If lxml is installed, you can use 'lxml'
    except Exception as e:
        return (False, f"Failed to parse the HTML content: {e}")
    
    scripts = soup.find_all('script')
    session_id = None
    for script in scripts:
        if script.string:
            match = re.search(r"this\.currentSessionID\s*=\s*'(\d+)'", script.string)
            if match:
                session_id = match.group(1)
                break
    if not session_id:
        return (False, "Session ID was not found.")
    print(f"Extracted sessionID: {session_id}")
    
    # 3. Construct the target URL with the extracted session ID
    base_url = "https://ehall.xjtu.edu.cn/jwapp/sys/frReport2/show.do"
    timestamp = int(time.time() * 1000)  # Current timestamp in milliseconds
    params = {
        '_': timestamp,
        '__boxModel__': 'true',
        'op': 'page_content',
        'sessionID': session_id,
        'pn': 1
    }
    query_string = urlencode(params)
    target_url = f"{base_url}?{query_string}"
    print(f"Constructed target URL: {target_url}")
    
    # 4. Set request headers (optional, recommended to simulate a browser)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
                      'AppleWebKit/537.36 (KHTML, like Gecko) ' \
                      'Chrome/112.0.0.0 Safari/537.36',
        'Referer': 'https://ehall.xjtu.edu.cn/login',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive'
    }
    
    # 5. Send GET request to the URL using the cookies and headers
    try:
        response = requests.get(target_url, cookies=cookies, headers=headers, timeout=10)
    except requests.exceptions.RequestException as e:
        return (False, f"Failed to send GET request: {e}")
    
    # 6. Check the response
    if response.status_code == 200:
        print("Successfully accessed the target URL")
        return (True, response.text)
    else:
        return (False, f"Request failed with status code: {response.status_code}")


if __name__ == "__main__":
    """
    Main function to read HTML content, call fetch_score_page, and handle the result.
    if -o <file> is specified, save the HTML content to a file.
    """
    
    if len(sys.argv) < 3:
        print("Usage: python fetchScore.py [cookies_file_path] [html_content_file_path]")
        sys.exit(1)

    # Parse command line arguments
    cookies_path = sys.argv[1]
    html_file_path = sys.argv[2]

    # Read HTML content from the specified file
    with open(html_file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Call fetch_score_page function
    success, result = fetch_score_page(cookies_path, html_content)

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
