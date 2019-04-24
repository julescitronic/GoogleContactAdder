from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/contacts']

def printLogo():
	print("============================");
	print("=Google Contacts adder v1.0=");
	print("= Made by Jules Hummelink  =");
	print("============================");
	print("                            ");

printLogo();
print("First of all, lets login to your google account");

creds = None
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

service = build('people', 'v1', credentials=creds)

os.system('clear');

printLogo();
print("Nice, now we are going to create a label for the contacts that we will be adding!");
label_name = raw_input("What name should I give the label?");

result = service.contactGroups().create(body={
	"contactGroup": {
    	"name":label_name
  	}
}).execute();

groupId = result.get("resourceName");

os.system("clear");

printLogo();
print("Now, lets start adding contacts to the label!");
print("                                             ");

userCount = "1";

while True:
        name = "*contact " + str(userCount);
        number = raw_input('Please enter the next phone number of contact ' + str(userCount) + ' ');
        service.people().createContact(parent='people/me', body={
            "names": [
                {
                    "givenName": name
                }
            ],
            "phoneNumbers": [
                {
                    'value': number
                }
            ],
            "memberships": [
                {
                    "contactGroupMembership":
                    { 
                        'contactGroupResourceName': groupId
                    }
                }
            ]

        }).execute()
        userCount = int(userCount) + 1;


