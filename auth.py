from base64 import urlsafe_b64encode
import hashlib
import json
import random
import re
import string
import requests
from time import sleep


class AuthClient(object):

    session = requests.session()

    defaultHeaders = {
        "Accept": "*/*",
        "Accept-Language": "en-us",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
        "Accept-Encoding": "gzip, deflate, br",
    }

    token_endpoint = "https://sso.ci.ford.de/v1.0/endpoint/default/token"

    def __init__(self, config):
        self.client_id      = config["FORD"]["CLIENT_ID"]
        self.application_id = config["FORD"]["APPLICATION_ID"]
        self.vin            = config["FORD"]["VIN"]
        
        self.redirect_uri = "https://www.ford.de/hilfe/fahrzeug-ueberblick?vin=" + self.vin
        
        
    def get_user_access_token(self, username, password):
        pkce_code = ''.join(random.choice(string.ascii_lowercase) for i in range(43))

        # Fetch the Auth URL
        authURL = self.web_session(pkce_code, self.redirect_uri, self.client_id)

        # Attempt to login
        codeURL = self.attemptLogin(authURL, username, password)

        # Fetch the auth codes
        codes = self.fetch_auth_codes(codeURL)

        headers = {
            **self.defaultHeaders,
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        data = {
            'client_id': self.client_id,
            'grant_type': 'authorization_code',
            "redirect_uri": self.redirect_uri,
            "grant_id": codes["grant_id"],
            "code": codes["code"], 
            "code_verifier": pkce_code
        }

        response = self.session.post(self.token_endpoint, headers=headers, data=data)

        if response.status_code == 200:
            result = response.json()
            if result["access_token"]:
                access_token = result["access_token"]
        else:
            raise Exception("Error Fetching Access Token with PKCE Code")

        if (access_token):

            headers['Content-Type'] = 'application/json'
            headers['Application-Id'] = self.application_id

            data = {
                'ciToken': access_token
            }

            sleep(5)       

            response = self.session.post('https://api.mps.ford.com/api/token/v2/cat-with-ci-access-token', headers=headers, data=json.dumps(data)).json()

            return response
        
        else:
            raise Exception("Access Token was not returned")

    def web_session(self, pkce_code, redirect_uri, client_id):
        headers = {
            **self.defaultHeaders,
            'Content-Type': 'application/json',
        }
        code_verifier = self.generate_hash(pkce_code)

        response = self.session.get("https://sso.ci.ford.de/v1.0/endpoint/default/authorize?redirect_uri=" + redirect_uri +"&response_type=code&scope=openid&max_age=3600&client_id="+ client_id +"&code_challenge=" + code_verifier + "&code_challenge_method=S256", headers=headers)

        authURL = re.findall('data-ibm-login-url="(.*)"\s', response.text)[0]
        if (authURL):
            return "https://sso.ci.ford.de" + authURL
        raise Exception("Missing AuthURL")

    def attemptLogin(self, authURL, username, password):
        headers = {
            **self.defaultHeaders,
            "Content-Type": "application/x-www-form-urlencoded",
        }
        
        data = {
            "operation": "verify",
            "login-form-type": "password",
            "username" : username,
            "password" : password
        }

        response = self.session.post(authURL, headers=headers, data=data, allow_redirects=False)

        if response.status_code == 302:
            return response.headers["Location"]
        raise Exception("Unable to login, missing location redirect")

    def fetch_auth_codes(self, codeURL):
        headers = {
            **self.defaultHeaders,
            'Content-Type': 'application/json',
        }

        response = self.session.get(codeURL, headers=headers, allow_redirects=False)

        if response.status_code == 302:
            nextUrl = response.headers["Location"]
            query = requests.utils.urlparse(nextUrl).query
            params = dict(x.split('=') for x in query.split('&'))
            code = params["code"]
            grant_id = params["grant_id"]

            return {
                "code": code,
                "grant_id": grant_id
            }
        raise Exception("Unable to Fetch Code & Grant ID")
            
    def base64UrlEncode(self,data):
        return urlsafe_b64encode(data).rstrip(b'=')
        
    def generate_hash(self, code):
        m = hashlib.sha256()
        m.update(code.encode('utf-8'))
        return self.base64UrlEncode(m.digest()).decode('utf-8')
        
