from kubernetes import client, config
import base64

def create_secret(api, namespace, embedding_secret_key):
    secret_name = "metabase-embedding-secret-key"
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
    configmap_name = "metabase-embedded-resource"
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

def create_k8s_resources(namespace, embedding_secret_key, resource_name, resource_number):
    config.load_incluster_config()
    client.configuration.assert_hostname = False

    v1 = client.CoreV1Api()
    create_secret(v1, namespace, embedding_secret_key)
    create_configmap(v1, namespace, resource_name, resource_number)