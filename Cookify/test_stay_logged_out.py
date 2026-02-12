
import os
import django
import sys
import json
from django.test import RequestFactory, Client
from django.urls import reverse

# Setup Django environment
sys.path.append('/home/hara/Program_Files/Python/Web_Apps/Cookify/Cookify')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Cookify.settings')
django.setup()

def test_stay_logged_out_logic():
    client = Client()
    
    response = client.get('/', HTTP_HOST='127.0.0.1')
    content = response.content.decode('utf-8')
    # Check for the HTML element specifically
    if '<div class="alert-container">' in content and 'Not Logged in !' in content:
        print("SUCCESS: Alert is present when not logged in.")
    else:
        print("FAIL: Alert is NOT present when not logged in.")
        
    # 2. Call prefer_logged_out endpoint
    print("Calling prefer_logged_out endpoint...")
    response = client.get('/cook/prefer-logged-out/', HTTP_HOST='127.0.0.1')
    if response.status_code == 200:
        data = json.loads(response.content)
        if data.get('status') == 'success':
            print("SUCCESS: Endpoint returned success.")
        else:
             print(f"FAIL: Endpoint returned unexpected data: {data}")
    else:
        print(f"FAIL: Endpoint returned status code {response.status_code}")
        
    # 3. Access home page again -> Alert should be hidden (or not present in a certain way depending on template check)
    # Since we modified the template to not render it if session var is set
    response = client.get('/', HTTP_HOST='127.0.0.1')
    content = response.content.decode('utf-8')
    # logic was: {% if not request.user.is_authenticated and not request.session.prefer_logged_out %}
    
    if '<div class="alert-container">' not in content:
        print("SUCCESS: Alert is ABSENT after setting preference.")
    else:
        print("FAIL: Alert is STILL PRESENT after setting preference.")
        # Print snippet around alert
        start = content.find('<div class="alert-container">')
        print(content[start:start+300])

if __name__ == '__main__':
    test_stay_logged_out_logic()
