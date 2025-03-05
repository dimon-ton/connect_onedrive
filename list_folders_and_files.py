import os
import httpx
from dotenv import load_dotenv
from ms_graph import get_access_token, MS_GRAPH_BASE_URL

def list_root_folder(headers):
    url = f'{MS_GRAPH_BASE_URL}/me/drive/root/children'
    response = httpx.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return [item for item in data['value']]
    else:
        print(f'Failed to list root folder: {response.status_code}')
        return []
    
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
        
        root_folder = list_root_folder(headers)

        for folder in root_folder:
            print(folder['name'])


    except Exception as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    main()