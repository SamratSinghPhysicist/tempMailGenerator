import requests
import time

class TempMail:
    def __init__(self):
        self.base_url = "https://api.mail.tm"
        
    def create_account(self):
        domain = requests.get(f"{self.base_url}/domains").json()['hydra:member'][0]['domain']
        email = f"temp{int(time.time())}@{domain}"
        password = "password123"
        
        data = {"address": email, "password": password}
        response = requests.post(f"{self.base_url}/accounts", json=data)
        
        if response.status_code == 201:
            print(f"Temporary Email Created: {email}")
            token = self.login(email, password)
            return {"email": email, "password": password, "token": token}
        else:
            print("Error creating email account.")
            return None
    
    def login(self, email, password):
        response = requests.post(f"{self.base_url}/token", json={"address": email, "password": password})
        if response.status_code == 200:
            return response.json()["token"]
        else:
            print("Error logging in.")
            return None
    
    def get_messages(self, account):
        headers = {"Authorization": f"Bearer {account['token']}"}
        response = requests.get(f"{self.base_url}/messages", headers=headers)
        
        if response.status_code == 200:
            messages = response.json()["hydra:member"]
            return messages
        else:
            print("Error fetching messages.")
            return []
    
    def get_message_details(self, account, message_id):
        headers = {"Authorization": f"Bearer {account['token']}"}
        response = requests.get(f"{self.base_url}/messages/{message_id}", headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            print("Error fetching message details.")
            return None

if __name__ == "__main__":
    temp_mail = TempMail()
    while True:
        account = temp_mail.create_account()
        if not account:
            break
        
        print("Waiting for emails...")
        start_time = time.time()
        while time.time() - start_time < 180:
            messages = temp_mail.get_messages(account)
            if messages:
                print("Received Emails:")
                for msg in messages:
                    details = temp_mail.get_message_details(account, msg['id'])
                    print(f"From: {msg['from']['address']}, Subject: {msg['subject']}")
                    if details:
                        print(f"Message: {details['text']}\n")
                break
            time.sleep(10)
        
        cont = input("Generate another email? (y/n): ")
        if cont.lower() != 'y':
            break
