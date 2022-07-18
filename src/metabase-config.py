import os
import sys

# Metabase URL Environment Variable
metabase_url_env = "METABASE_URL"

def getMetabaseURL():
    # Default value for the Metabase URL
    metabase_url = ""

    try:
        if os.environ[metabase_url_env]:
            metabase_url = os.environ[metabase_url_env]
            print(metabase_url)
    except KeyError:
        print(metabase_url_env, ' environment variable not set.')
        sys.exit(1)
    
    return metabase_url

getMetabaseURL()