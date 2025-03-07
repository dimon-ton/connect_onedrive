import os
import requests
from ms_graph import MS_GRAPH_BASE_URL
from example2 import generate_access_token


APP_ID = os.getenv('APPLICATION_ID')
SCOPES = ['Files.ReadWrite']

access_token = generate_access_token(APP_ID, SCOPES)
print(access_token)
headers = {
    'Authorization': 'Bearer ' + access_token['access_token']
}

file_path = r'C:\Users\saich\Documents\connect_onedrive\qr_code.jpg'
file_name = os.path.basename(file_path)


onedrive_folder_id = '8E3E5A1607340544%21282282'

with open(file_path, 'rb') as upload:
    media_content = upload.read()

response = requests.put(
    MS_GRAPH_BASE_URL + f'/me/drive/items/{onedrive_folder_id}:/{file_name}:/content',
    headers=headers,
    data=media_content
)
