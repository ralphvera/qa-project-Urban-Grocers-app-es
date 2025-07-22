import configuration
import requests
import data

def post_new_user(body):
    return requests.post(configuration.URL_SERVICE + configuration.CREATE_USER_PATH,
                         json=body,
                         headers=data.headers)

def post_new_kit(kit_body, auth_token):
    # 1. Copiamos los headers base de data.py para no modificarlos directamente
    kit_headers = data.headers.copy()
    kit_headers["Authorization"] = f"Bearer {auth_token}"
    return requests.post(configuration.URL_SERVICE + configuration.KITS_PATH,
                         json=kit_body,
                         headers=kit_headers)

def get_users_table():
    return requests.get(configuration.URL_SERVICE + configuration.USERS_TABLE_PATH)