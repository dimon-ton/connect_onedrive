import os
import sys
import msal
import requests

class NonInteractiveAuth:
    def __init__(self, client_id, tenant_id, client_secret):
        """
        Initialize non-interactive authentication
        
        Args:
            client_id (str): Azure AD application client ID
            tenant_id (str): Azure AD tenant ID
            client_secret (str): Client secret for authentication
        """
        self.client_id = client_id
        self.tenant_id = tenant_id
        self.client_secret = client_secret
        
        # Authority URL for token acquisition
        self.authority = f'https://login.microsoftonline.com/{tenant_id}'
    
    def get_access_token(self, scopes):
        """
        Obtain access token without user interaction
        
        Args:
            scopes (list): List of required permission scopes
        
        Returns:
            str: Access token for API requests
        """
        try:
            # Create Confidential Client Application
            app = msal.ConfidentialClientApplication(
                self.client_id,
                authority=self.authority,
                client_credential=self.client_secret
            )
            
            # Acquire token for client (app-only access)
            result = app.acquire_token_for_client(scopes=scopes)
            
            # Check if token acquisition was successful
            if 'access_token' in result:
                return result['access_token']
            else:
                # Detailed error logging
                error = result.get('error')
                error_description = result.get('error_description')
                print(f"Token Acquisition Failed - Error: {error}")
                print(f"Description: {error_description}")
                raise ValueError("Failed to obtain access token")
        
        except Exception as e:
            print(f"Authentication error: {e}")
            raise

def main():
    # Retrieve credentials from environment variables
    try:
        CLIENT_ID = os.environ['APPLICATION_ID']
        TENANT_ID = os.environ['TENANT_ID']
        CLIENT_SECRET = os.environ['CLIENT_SECRET']
    except KeyError as e:
        print(f"Missing environment variable: {e}")
        print("Set APPLICATION_ID, TENANT_ID, and CLIENT_SECRET")
        sys.exit(1)
    
    # Define required scopes
    SCOPES = [
        'https://graph.microsoft.com/.default'  # Use .default for app-only access
    ]
    
    try:
        # Initialize non-interactive authentication
        auth = NonInteractiveAuth(CLIENT_ID, TENANT_ID, CLIENT_SECRET)
        
        # Get access token
        access_token = auth.get_access_token(SCOPES)
        
        print("Successfully obtained access token")
        
        # Optional: Verify token by making a simple Microsoft Graph request
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        # Example: Get user profile (replace with your specific use case)
        response = requests.get(
            'https://graph.microsoft.com/v1.0/users', 
            headers=headers
        )
        
        print("Graph API Response Status:", response.status_code)
    
    except Exception as e:
        print(f"Authentication process failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()