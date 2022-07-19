import sys
from urllib import response
import requests

def create_card(mb_url, session_id, dashboard_id):
    card_url = "{}/api/dashboard/{}/cards".format(mb_url, dashboard_id)
    card_id = -1

    card_id_response = requests.post(card_url,
        cookies = {
            "metabase.SESSION": session_id
        },
        json = {
            "cardid": None
        })
    
    if card_id_response.ok:
        card_id = card_id_response.json()["id"]
    else:
        print("ERROR: {}".format(response.text))
        sys.exit(1)

    create_card_response = requests.put(card_url,
        cookies = {
            "metabase.SESSION": session_id
        },
        json = {"cards":[
                {
                    "id": card_id,
                    "row":0,
                    "col":0,
                    "sizeX":4,
                    "sizeY":4,
                    "series":[],
                    "parameter_mappings":[],
                    "visualization_settings":{
                        "virtual_card":{
                            "display":"text",
                            "visualization_settings":{},
                            "dataset_query":{},
                            "archived": False
                        },
                        "text":"This dashboard should be edited in future in order to populate actual metrics."
                    }
                }
            ]})

    if create_card_response.ok and create_card_response.json()["status"] == "ok":
        print("INFO: Successfully created card on dashboard")
    else:
        print("ERROR: {}".format(create_card_response.text))
        sys.exit(1)

def enable_dashboard_embedding(mb_url, session_id, dashboard_id):
    url = "{}/api/dashboard/{}".format(mb_url, dashboard_id)

    response = requests.put(url,
        cookies = {
            "metabase.SESSION": session_id
        },
        json = {
            "enable_embedding": True,
            "embedding_params": {}
        })
    
    if response.ok and response.json()["enable_embedding"] == True:
        print("DEBUG: Successfully enabled embedding on Dashboard {}".format(dashboard_id))
    else:    
        print("ERROR: {}".format(response.text))
        sys.exit(1)
    


def create_dashboard(mb_url, session_id):
    dashboard_url = "{}/api/dashboard".format(mb_url)
    dashboard_id = -1

    create_dashboard_response = requests.post(dashboard_url,
        cookies = {
            "metabase.SESSION": session_id
        },
        json = {
            "collection_id": 1,
            "description": "This is the default dashboard rendered on the iNSight frontend microservice",
            "name": "Default iNSight Dashboard"
        })
    
    if create_dashboard_response.ok:
        dashboard_id = create_dashboard_response.json()["id"]
        print("INFO: Successfully created dashboard.")
        create_card(mb_url, session_id, dashboard_id)
        enable_dashboard_embedding(mb_url, session_id, dashboard_id)
    else:
        print("ERROR: {}".format(create_dashboard_response.text))
        sys.exit(1)

    return dashboard_id