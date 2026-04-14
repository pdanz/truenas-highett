import os
import requests
import urllib3
from dotenv import load_dotenv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()

HOST = os.environ["TRUENAS_HOST"]
PORT = os.environ.get("TRUENAS_PORT", "20443")
HOSTNAME = os.environ.get("TRUENAS_HOSTNAME", HOST)
API_KEY = os.environ.get("TRUENAS_API_KEY")
BASE_URL = f"https://{HOST}:{PORT}/api/v2.0"


def _make_session(auth_header=None, basic_auth=None):
    s = requests.Session()
    s.headers.update({"Host": HOSTNAME})
    s.verify = False  # self-signed cert — intentional on local network
    if auth_header:
        s.headers.update({"Authorization": auth_header})
    if basic_auth:
        s.auth = basic_auth
    return s


def login(username, password):
    """Authenticate with username/password. Returns a new session."""
    s = _make_session(basic_auth=(username, password))
    r = s.get(f"{BASE_URL}/system/info")
    r.raise_for_status()
    return s


# Default session authenticated via API key
session = _make_session(auth_header=f"Bearer {API_KEY}") if API_KEY else None


def get(endpoint, **params):
    r = session.get(f"{BASE_URL}/{endpoint}", params=params)
    r.raise_for_status()
    return r.json()


def post(endpoint, payload=None):
    r = session.post(f"{BASE_URL}/{endpoint}", json=payload)
    r.raise_for_status()
    return r.json()


if __name__ == "__main__":
    import os

    # Test API key auth
    print("--- API key auth ---")
    info = get("system/info")
    print(f"Hostname : {info['hostname']}")
    print(f"Version  : {info['version']}")
    print(f"Uptime   : {info['uptime']}")

    # Test username/password auth
    username = os.environ.get("TRUENAS_USER", "admin")
    password = os.environ.get("TRUENAS_PASSWORD")
    if password:
        print("\n--- Username/password auth ---")
        s = login(username, password)
        r = s.get(f"{BASE_URL}/system/info")
        info2 = r.json()
        print(f"Hostname : {info2['hostname']}")
        print(f"Version  : {info2['version']}")
        print("Login successful")
    else:
        print("\nSet TRUENAS_USER / TRUENAS_PASSWORD in .env to test password auth")
