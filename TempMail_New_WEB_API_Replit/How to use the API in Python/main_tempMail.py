import requests
import time

# Base URL of the API
API_MAIN_DOMAIN = "https://mailtemp-production.up.railway.app/"   #URL of MailTemp Website
BASE_URL = f"{API_MAIN_DOMAIN}api"    #In this case: https://mailtemp-production.up.railway.app/api

def create_temp_email():
    """Create a temporary email address"""
    response = requests.post(f"{BASE_URL}/email")
    if response.status_code == 200:
        return response.json()
    raise Exception(f"Failed to create email: {response.json()['message']}")

def get_messages(email_id):
    """Get messages for a specific email ID"""
    response = requests.get(f"{BASE_URL}/email/{email_id}/messages")
    if response.status_code == 200:
        return response.json()
    raise Exception(f"Failed to get messages: {response.json()['message']}")

def main():
    # Create a temporary email
    email = create_temp_email()
    print(f"Created email: {email['address']}")
    
    # Poll for new messages every 5 seconds
    while True:
        messages = get_messages(email['id'])
        for message in messages:
            print("\nNew message:")
            print(f"From: {message['from']}")
            print(f"Subject: {message['subject']}")
            print(f"Content: {message['content']}")
        
        time.sleep(5)  # Wait 5 seconds before checking again

if __name__ == "__main__":
    main()
