import requests
import json
import logging
import sys
import os

# Setup logging
logger = logging.Logger(__name__)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


def read_config(config_filename):
    ''' Read config file, return json with parameters
    '''

    try:
        with open(config_filename, "r") as config_file:
            config_data = json.load(config_file)
            return config_data

    except FileNotFoundError:
        logger.error("Config file do not exists, exiting.")
   
def get_auth_token(base_url, auth_endpoint, content_type, username, password):
    '''Sends auth POST request, returns auth token
    '''

    auth_url = f"{base_url}/{auth_endpoint}"
    headers = {"content-type": content_type}
    payload = {"username": username, "password": password}

    logger.debug(f"Sending auth request to {auth_url}")

    try:
        auth_response = requests.post(auth_url, json=payload, headers=headers)
        auth_response.raise_for_status()

        data = json.loads(auth_response.content)
        
        return data.get("access_token")

    except requests.HTTPError as e:
        logger.error(f"Auth request to {auth_url} failed with {e.args}")

def get_data(base_url, out_endpoint, jwt_token, content_type, date_to_extract):
    '''Get data from the API for specified day(s)
    '''
    data_url = f"{base_url}/{out_endpoint}"
    headers = {"content-type": content_type, "Authorization": jwt_token}
    payload = date_to_extract

    logger.debug(f"Sending data request to {data_url}")

    try:
        data_response = requests.get(data_url, json=payload, headers=headers)
        data_response.raise_for_status()

        data = json.loads(data_response.content)

        return data

    except requests.HTTPError as e:
        logger.error(f"Data request to {data_url} failed with {e.args}")

def process_data(data, date_to_extract):
    ''' Process data, save to local files
    '''
    date = date_to_extract.get("date")
    folder = f"./data/{date}"

    if not os.path.exists(folder):
        os.makedirs(folder)

    with open(f"{folder}/data.json", "w+") as output_file:
       json.dump(data, output_file, indent=4)
       logger.debug(f"Data saved to {folder}/data.json")

############################################

if __name__ == "__main__":

    config_data = read_config("config.json")

    if not config_data:
        sys.exit()

    # Get parameters
    base_url = config_data.get("base_url")
    auth_endpoint = config_data.get("auth_endpoint")
    out_endpoint = config_data.get("out_endpoint")
    auth_type = config_data.get("auth_type")
    content_type = config_data.get("content_type")
    username = config_data.get("username")
    password = config_data.get("password")
    date_to_extract = config_data.get("date_to_extract")
    
    # Get auth token
    token = get_auth_token(base_url, auth_endpoint, content_type, username, password)

    if token:
        jwt_token = f"{auth_type} {token}"

        # Request data
        data = get_data(base_url, out_endpoint, jwt_token, content_type, date_to_extract)
        
        if not data:
            logger.error("No data returned, exiting")
            sys.exit()

        # Finally process data and save to file
        process_data(data, date_to_extract)