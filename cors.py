try:
    import argparse
    import concurrent.futures
    import os
    import random
    import requests
    import sys
    import time
except ImportError:
    os.system("pip3 install requests")


def main():
    try:
        os.system("clear")
        print("   __   __   __   __  ")
        print("  /  ` /  \ |__) /__` ")
        print("  \__, \__/ |  \ .__/ ")
        print("   @nmochea          \n")
        
        parser = argparse.ArgumentParser()
        parser.add_argument('-file', help='File containing URLs', required=True)
        args = parser.parse_args()
        file_name = args.file
        
        with open(file_name, "r") as file:
            urls = file.read().splitlines()

        if len(urls) == 0:
            print("No URLs found in the file")
            sys.exit(1)

        if len(urls) > 1:
            print(f"Starting scan for {len(urls)} URLs...\n")

        payloads = [
            {"Origin": "https://evil.com"},
            {"Origin": "null"},
            {"Origin": "*"}
        ]
        custom_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53." + str(random.randint(0, 99999)),
            "Accept": "text/html, */*",
            "Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/x-www-form-urlencoded",
            "Connection": "clsoe"
        }

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            for url in urls:
                for payload in payloads:
                    payload.update(custom_headers)
                    executor.submit(scan_url, url, payload)

    except FileNotFoundError:
        print(f"File {file_name} not found")
        sys.exit(1)

def scan_url(url, payload):
    try:
        response = requests.get(url, headers=payload, allow_redirects=False, timeout=15)
        if "Access-Control-Allow-Origin" in response.headers:
            if "google.com" in response.headers["Access-Control-Allow-Origin"]:
                print("[CORS] " + url)
            elif response.headers["Access-Control-Allow-Origin"] == "null":
                print("[Null] " + url)
            elif response.headers["Access-Control-Allow-Origin"] == "*":
                print("[Wildcard] " + url)

    except Exception as e:
        pass

if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"\nElapsed time: {time.time() - start_time:.2f} seconds")

