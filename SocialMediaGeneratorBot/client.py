import requests


class API_Client:
    def __init__(self, base_url):
        self.base_url = base_url
        self.jwt_token = None

    def _get_headers(self):
        headers = {"Content-Type": "application/json"}
        if self.jwt_token:
            headers["Authorization"] = f"Bearer {self.jwt_token}"
        return headers

    def _login(self, user):
        login_url = f"{self.base_url}/auth/login"
        credentials = {"email": user["email"], "password": user["password"]}
        try:
            response = requests.post(login_url, json=credentials)
            response.raise_for_status()  # Check the response status
            self.jwt_token = response.json().get("access_token")
            return self.jwt_token
        except requests.exceptions.RequestException as e:
            return None

    def post(self, endpoint, payload=None, user=None):
        url = f"{self.base_url}/{endpoint}"
        headers = self._get_headers()
        response = None

        try:
            response = requests.post(url, json=payload, headers=headers)

            if response.status_code == 401 or response.status_code == 500:
                # Try to re-authenticate
                login_response = self._login(user)
                if login_response:
                    # Retry the request with the updated token
                    headers = self._get_headers()
                    response = requests.post(url, json=payload, headers=headers)
                else:
                    # Return the response to handle it in the calling code
                    return response

            response.raise_for_status()  # Check the response status
            self.jwt_token = None
            return response
        except requests.exceptions.RequestException as e:
            return response

    def get(self, endpoint, payload=None, user=None):
        url = f"{self.base_url}/{endpoint}"
        headers = self._get_headers()
        response = None

        try:
            response = requests.get(url, json=payload, headers=headers)

            if response.status_code == 401 or response.status_code == 500:
                # Try to re-authenticate
                login_response = self._login(user)
                if login_response:
                    # Retry the request with the updated token
                    headers = self._get_headers()
                    response = requests.get(url, json=payload, headers=headers)
                else:
                    # Return the response to handle it in the calling code
                    return response

            response.raise_for_status()  # Check the response status
            self.jwt_token = None
            return response
        except requests.exceptions.RequestException as e:
            return response
