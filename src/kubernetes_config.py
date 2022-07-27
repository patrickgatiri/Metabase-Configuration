from kubernetes import client, config
import base64

configmap_name = "metabase-embedded-resource"
secret_name = "metabase-embedding-secret-key"

configmap_name = "vault-operator-lock"
secret_name = "vault-server-unseal-keys"

def create_secret(api, namespace, embedding_secret_key):
    secret_key = "embedding-secret-key"

    secret = client.V1Secret()

    secret.metadata = client.V1ObjectMeta(name = secret_name, namespace = namespace)
    secret.type = "Opaque"
    secret.data = {
        secret_key: base64.b64encode(embedding_secret_key.encode('ascii')).decode("utf-8")
    }

    api_response = api.create_namespaced_secret(namespace = namespace, body = secret)
    if client.ApiClient().sanitize_for_serialization(api_response)["kind"] == "Secret":
        print("INFO: Secret created under the name \"{}\"".format(client.ApiClient().sanitize_for_serialization(api_response)["metadata"]["name"]))

def create_configmap(api, namespace, resource_name, resource_number):
    resource_name_key = "resource-name"
    resource_number_key = "resource-number"

    configmap = client.V1ConfigMap()
    configmap.metadata = client.V1ObjectMeta(name = configmap_name, namespace = namespace)
    configmap.data = {
        resource_name_key: resource_name,
        resource_number_key: resource_number
    }

    api_response = api.create_namespaced_config_map(namespace = namespace, body = configmap)
    if client.ApiClient().sanitize_for_serialization(api_response)["kind"] == "ConfigMap":
        print("INFO: ConfigMap created under the name \"{}\"".format(client.ApiClient().sanitize_for_serialization(api_response)["metadata"]["name"]))

def secret_exists(api, namespace, secret_name):
    response = api.list_namespaced_secret(namespace=namespace)
    for secret in response.items:
        if secret.metadata.name == secret_name:
            return True
    return False

def configmap_exists(api, namespace, configmap_name):
    response = api.list_namespaced_config_map(namespace=namespace)
    for configmap in response.items:
        if configmap.metadata.name == configmap_name:
            return True
    return False

def create_k8s_resources(namespace, embedding_secret_key, resource_name, resource_number):
    # config.load_incluster_config()
    config.load_kube_config()
    client.configuration.assert_hostname = False

    v1 = client.CoreV1Api()

    if not secret_exists(v1, namespace, secret_name):
        create_secret(v1, namespace, embedding_secret_key)
    else:
        print("ERROR: Cannot create secret. Secret \"{}\" in namespace \"{}\" already exists.".format(secret_name, namespace))

    if not configmap_exists(v1, namespace, configmap_name):
        create_configmap(v1, namespace, resource_name, resource_number)
    else:
        print("ERROR: Cannot create configmap. Configmap \"{}\" in namespace \"{}\" already exists".format(configmap_name, namespace))

create_k8s_resources("vault", "123", "dashboard", "1")