import requests
import sys

def get_setup_token(mb_url):
    url = "{}/api/session/properties".format(mb_url)
    return requests.get(url).json()["setup-token"]

def get_session_id(mb_url, mb_user):
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
    else:
        print("ERROR: Failure creating initial user")
        sys.exit(1)
    
    return session_id