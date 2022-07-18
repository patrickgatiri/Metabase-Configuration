import os
import sys
import requests

# Environment Variables
metabase_host_env = "MB_HOST"
metabase_port_env = "MB_PORT"
metabase_protocol_env = "MB_PROTOCOL"

def build_connection_string(metabase_protocol, metabase_host, metabase_port):
    return "{}://{}:{}"/format(metabase_protocol, metabase_host, metabase_port)

def getEnvVariable(env_variable_name):
    try:
        if os.environ[env_variable_name]:
            metabase_url = os.environ[env_variable_name]
            print(metabase_url)
    except KeyError:
        print(env_variable_name, ' environment variable not set.')
        sys.exit(1)
    
    return metabase_url

metabase_protocol = getEnvVariable(metabase_protocol_env)
metabase_host = getEnvVariable(metabase_host_env)
metabase_port = getEnvVariable(metabase_port_env)