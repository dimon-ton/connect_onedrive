import os
import webbrowser
import msal
from dotenv import load_dotenv


MS_GRAPH_BASE_URL = 'https://graph.microsoft.com/v1.0'

def get_access_token(app_id, client_secret, scopes):
    client = msal.ConfidentialClientApplication(
        client_id=app_id,
        client_credential=client_secret,
        authority='https://login.microsoftonline.com/consumers/',
    )

    auth_request_url = client.get_authorization_request_url(scopes)
    webbrowser.open(auth_request_url)
    authorization_code = input('Enter the authorization code: ')

    token_response = client.acquire_token_by_authorization_code(
        code=authorization_code,
        scopes=scopes
    )

    if 'access_token' in token_response:
        return token_response['access_token']
    else:
        raise Exception('Failed to obtain access token' + str(token_response))
    
def main():
    load_dotenv() 
    APPLICATION_ID = os.getenv('APPLICATION_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    SCOPES = ['User.Read', 'Files.ReadWrite.ALL']

    try:
        access_token = get_access_token(app_id=APPLICATION_ID, client_secret=CLIENT_SECRET, scopes=SCOPES)
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        print(headers)
    except Exception as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    main()

