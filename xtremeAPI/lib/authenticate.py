
import requests as req

from . import loadConfig



def generate_token():
    '''
    Login to Xtreme API via OAuth2.0 by generating access token      
    '''

    credentials = loadConfig.get_b64_credentials()
    payload = {'grant_type': 'password',
               'username': credentials["username"],
               'password': credentials["password"],
               }

    token_url = loadConfig.get_urls()["token"]

    res = req.post(url=token_url, data=payload)
    if (res.status_code != 200):
        return {"success": False, "res": res}
        
    access_token = res.json()['access_token']
    return {"success": True, "token": access_token}



def submit_request(url, payload, token):
    ''' Submit the request to the REST API with the correct headers
    '''
    headers = { 'Authorization': 'bearer ' + token,
                'Content-Type': 'application/octet-stream'}

    res = req.post(url=url, headers=headers, data=payload)

    if (res.status_code != 200):
        return {"success": False, "res": res}
        
    return {"success": True, "result": res.content}

