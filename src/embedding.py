import requests
import sys

def enable_embedding(mb_url, session_id):
    url = "{}/api/setting/enable-embedding".format(mb_url)

    response = requests.put(url,
        cookies = {
            "metabase.SESSION": session_id
        },
        json = {
            "value": True
        })

    # Successful request prompts no response from the Metabase server
    if not response.ok:
        print("ERROR: {}". format(response.text))
        sys.exit(1)
    else:
        print("INFO: Successfully enabled embedding on the Metabase server")

def set_embedding_secret(mb_url, session_id):
    enable_embedding(mb_url, session_id)
    embedding_secret_key = requests.get("{}/api/util/random_token".format(mb_url)).json()["token"]

    url = "{}/api/setting/embedding-secret-key".format(mb_url)
    response = requests.put(url,
        cookies = {
            "metabase.SESSION": session_id
        },
        json = {
            "value": embedding_secret_key
        })
    
    # Successful request prompts no response from the Metabase server
    if not response.ok:
        print("ERROR: {}". format(response.text))
        sys.exit(1)
    else:
        print("INFO: Successfully set embedding secret on the Metabase server")
    
    return embedding_secret_key