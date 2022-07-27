import os
import sys

# Custom defined modules
import user
import embedding
import dashboard
import kubernetes_config

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

# Kubernetes namespace
mb_namespace_env = "MB_NS"

# Reads environment variables
def getEnvVariable(env_variable_name):
    try:
        if os.environ[env_variable_name]:
            env_value = os.environ[env_variable_name]
            if not env_variable_name == mb_user_pass_env:
                print("INFO: Using {} as {}".format(env_variable_name, env_value))
    except KeyError:
        print("ERROR: {} environment variable not set.".format(env_variable_name))
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

    mb_namespace = getEnvVariable(mb_namespace_env)

    mb_url = build_connection_string(mb_protocol, mb_host, mb_port)
    session_id = None

    if not user.initial_user_exists:
        session_id = user.create_new_user(mb_url, mb_user)
    else:
        session_id = user.login_existing_user(mb_url, mb_user_email, mb_user_pass)

    print("DEBUG: Using session ID - {}".format(session_id))

    embedding_secret_key = embedding.set_embedding_secret(mb_url, session_id)
    resource_name = "dashboard"
    resource_number = dashboard.create_dashboard(mb_url, session_id)
    print("DEBUG: Embedding secret key - {}".format(embedding_secret_key))
    print("DEBUG: Resource name - {}".format(resource_name))
    print("DEBUG: Resource number - {}".format(resource_number))

    kubernetes_config.create_k8s_resources(mb_namespace, embedding_secret_key, resource_name, str(resource_number))

initial_config()