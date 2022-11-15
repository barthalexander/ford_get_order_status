import requests

def send_request(config, token):
    # cURL
    # GET https://www.digitalservices.ford.com/owner/api/v2/vehicle/order-status

    try:
        response = requests.get(
            url="https://www.digitalservices.ford.com/owner/api/v2/vehicle/order-status",
            params={
                "vin": config["FORD"]["VIN"],
                "countryCode": "DEU",
            },
            headers={
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "en-US,en;q=0.9",
                "Auth-Token": token,
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Consumer-Key": "Z28tZXUtZm9yZA==",
                "Dnt": "1",
                "Origin": "https://www.ford.de",
                "Pragma": "no-cache",
                "Referer": "https://www.ford.de/",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "cross-site",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
                "Sec-Ch-Ua": "\"Chromium\";v=\"107\", \"Not=A?Brand\";v=\"24\"",
                "Sec-Ch-Ua-Mobile": "?0",
                "Sec-Ch-Ua-Platform": "\"macOS\"",
                "Accept-Encoding": "gzip",
            },
        )
        return response.json()
    except requests.exceptions.RequestException:
        return ""
