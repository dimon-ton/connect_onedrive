import os
import requests
from dotenv import load_dotenv

class MicrosoftGraphClient:
    def __init__(self, access_token):
        self.access_token = access_token
        self.base_url = 'https://graph.microsoft.com/v1.0'
        self.headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

    def get_user_profile(self):
        """Retrieve the current user's profile"""
        url = f'{self.base_url}/me'
        response = requests.get(url, headers=self.headers)
        return self._handle_response(response)

    def list_drive_items(self, drive_id=None):
        """List items in OneDrive"""
        if drive_id:
            url = f'{self.base_url}/drives/{drive_id}/root/children'
        else:
            url = f'{self.base_url}/me/drive/root/children'
        
        response = requests.get(url, headers=self.headers)
        return self._handle_response(response)

    def upload_file(self, file_path, destination_path='/drive/root:/{filename}'):
        """Upload a file to OneDrive"""
        filename = os.path.basename(file_path)
        upload_url = f'{self.base_url}/me{destination_path.format(filename=filename)}:/content'
        
        with open(file_path, 'rb') as file:
            response = requests.put(
                upload_url, 
                headers={
                    **self.headers,
                    'Content-Type': 'application/octet-stream'
                },
                data=file
            )
        return self._handle_response(response)

    def send_email(self, recipient, subject, body):
        """Send an email using Microsoft Graph"""
        url = f'{self.base_url}/me/sendMail'
        email_data = {
            'message': {
                'subject': subject,
                'body': {
                    'contentType': 'Text',
                    'content': body
                },
                'toRecipients': [
                    {
                        'emailAddress': {
                            'address': recipient
                        }
                    }
                ]
            }
        }
        
        response = requests.post(url, headers=self.headers, json=email_data)
        return self._handle_response(response)

    def _handle_response(self, response):
        """Handle API responses"""
        try:
            response.raise_for_status()
            return response.json() if response.content else {"status": "Success"}
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
            print(f"Response Content: {response.text}")
            raise

def main():
    # Load environment variables
    load_dotenv()
    
    # Assume you've already obtained the access token
    ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')  # Or however you obtained the token
    
    # Create a Microsoft Graph client
    graph_client = MicrosoftGraphClient(ACCESS_TOKEN)
    
    try:
        # Example usage methods
        
        # 1. Get User Profile
        print("User Profile:")
        user_profile = graph_client.get_user_profile()
        print(user_profile)
        
        # 2. List OneDrive Files
        print("\nOneDrive Files:")
        drive_items = graph_client.list_drive_items()
        print(drive_items)
        
        # 3. Upload a File (uncomment and provide actual file path)
        # print("\nUploading File:")
        # upload_result = graph_client.upload_file('/path/to/your/file.txt')
        # print(upload_result)
        
        # 4. Send an Email (uncomment and provide actual email details)
        # print("\nSending Email:")
        # email_result = graph_client.send_email(
        #     recipient='recipient@example.com', 
        #     subject='Test Email', 
        #     body='This is a test email sent via Microsoft Graph API'
        # )
        # print(email_result)
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()