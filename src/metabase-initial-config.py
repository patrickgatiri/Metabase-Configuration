import os
import sys

import user_setup

### Environment Variables ###
# Metabase URL
mb_host_env = "MB_HOST"
mb_port_env = "MB_PORT"
mb_protocol_env = "MB_PROTOCOL"

# Metabase User
mb_user_email_env = "MB_USER_EMAIL"
mb_user_pass_env = "MB_USER_PASS"
mb_user_fname_env = "MB_USER_FNAME"
mb_user_lname_env = "MB_USER_LNAME"

# Reads environment variables
def getEnvVariable(env_variable_name):
    try:
        if os.environ[env_variable_name]:
            env_value = os.environ[env_variable_name]
            if not env_variable_name == mb_user_pass_env:
                print("Using {} as {}".format(env_variable_name, env_value))
    except KeyError:
        print("{} environment variable not set.".format(env_variable_name))
        sys.exit(1)
    
    return env_value

# Creates root URL to the metabase instance
def build_connection_string(mb_protocol, mb_host, mb_port):
    return "{}://{}:{}".format(mb_protocol, mb_host, mb_port)

def initial_config():
    mb_protocol = getEnvVariable(mb_protocol_env)
    mb_host = getEnvVariable(mb_host_env)
    mb_port = getEnvVariable(mb_port_env)

    mb_user_email = getEnvVariable(mb_user_email_env)
    mb_user_pass = getEnvVariable(mb_user_pass_env)
    mb_user_fname = getEnvVariable(mb_user_fname_env)
    mb_user_lname = getEnvVariable(mb_user_lname_env)
    mb_user = {
        "email": mb_user_email,
        "password": mb_user_pass,
        "first_name": mb_user_fname,
        "last_name": mb_user_lname,
        "site_name": "PREVOIR"
    }

    mb_url = build_connection_string(mb_protocol, mb_host, mb_port)
    sessionID = user_setup.getSessionID(mb_url, mb_user)