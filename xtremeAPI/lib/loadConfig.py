import base64
import os
import configparser


directoryPath = os.path.dirname(os.path.realpath(__file__)) + "/"
confFile    = directoryPath + "../config/configuration.ini"
config = configparser.RawConfigParser()


def read_config():    
    config.read(confFile)


def get_params():
    ''' This function sets values to all the attributes
              and configurations parameters.
        Credentials are encoded to Ascii in order to convert
              them to base64 later on.
    '''
    params = {}
    read_config()

    params["xtreme_env"]  = config.get("general", "env") # Xtreme_preprod || Xtreme_prod
    params["username"]    = config.get(params["xtreme_env"], "username").encode('ascii')
    params["password"]    = config.get(params["xtreme_env"], "password").encode('ascii')
    params["url"]         = config.get(params["xtreme_env"], "url")
    
    return params


def get_b64_credentials():
    ''' Returns base64 encoded values of username and password
    '''

    params = get_params()
    b64_username = base64.b64encode(params["username"]).decode()
    b64_password = base64.b64encode(params["password"]).decode()
    return {"username": b64_username, "password": b64_password}


def get_urls():
    ''' Returns on object containing all API urls'''
    
    urls = {}
    base_url  = get_params()["url"]
    
    urls["token"]    = base_url + config.get("endpoints", "token")
    urls["update"]   = base_url + config.get("endpoints", "update")
    urls["create"]   = base_url + config.get("endpoints", "create")
    urls["customer"] = base_url + config.get("endpoints", "customer")  

    return urls


