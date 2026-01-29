import os
import sys
import urllib3
from atlassian import Bitbucket
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

url = os.getenv('BITBUCKET_URL')
username = os.getenv('BITBUCKET_USERNAME')
password = os.getenv('BITBUCKET_PASSWORD')
target_project_key = os.getenv('BITBUCKET_PROJECT_KEY')
verify_ssl = os.getenv('BITBUCKET_VERIFY_SSL', 'True').lower() == 'true'

if not verify_ssl:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

bitbucket = Bitbucket(
    url=url,
    username=username,
    password=password,
    verify_ssl=verify_ssl
)

print(f"Checking connection to {url}...")
try:
    # Try to list projects
    projects = bitbucket.project_list()
    print("Found projects:")
    found = False
    for p in projects:
        print(f" - {p['key']} ({p['name']})")
        if p['key'] == target_project_key:
            found = True

    if found:
        print(f"\nSuccess: Project '{target_project_key}' found in the list.")
    else:
        print(f"\nError: Project '{target_project_key}' NOT found in the list.")

except Exception as e:
    print(f"Error accessing Bitbucket: {e}")
