import requests
import sys

def initial_user_exists(mb_url):
    url = "{}/api/session/properties".format(mb_url)
    return requests.get(url).json()["has-user-setup"]

def get_setup_token(mb_url):
    url = "{}/api/session/properties".format(mb_url)
    return requests.get(url).json()["setup-token"]

def create_new_user(mb_url, mb_user):
    url = "{}/api/setup".format(mb_url)

    setup_token = get_setup_token(mb_url)
    session_id = ""

    response = requests.post(url,
        headers = {"Content-Type": "application/json"},
        json = {
            "token": setup_token,
            "invite": "null",
            "user": mb_user,
            "prefs": {
                "allow_tracking": False,
                "site_locale": "en",
                "site_name": "PREVOIR"
            }
        })
    if response.ok:
        session_id = response.json()["id"]
        print("INFO: Initial user created")
    else:
        print("ERROR: Failure creating initial user")
        print(response.text)
        sys.exit(1)
    
    return session_id

def login_existing_user(mb_url, mb_user_email, mb_user_pass):
    print("INFO: Logging in as an existing user")
    
    url = "{}/api/session".format(mb_url)
    session_id = ""

    response = requests.post(url,
                         json={
                            'username': mb_user_email,
                            'password': mb_user_pass
                        })

    if response.ok:
        session_id = response.json()['id']
    else:
        print("ERROR: Cannot retrieve session ID from metabase server")
        print(response.text)
        sys.exit(1)

    return session_id