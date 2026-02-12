
import os
import django
import sys
from django.conf import settings
from unittest.mock import MagicMock

# Setup Django environment
sys.path.append('/home/hara/Program_Files/Python/Web_Apps/Cookify/Cookify')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Cookify.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.auth.models import User
from cooks.views import handle_error

# Verify handle_error logic (cannot easily run full view test without server, but can test function unit)
def test_handle_error_user_deletion():
    print("Testing handle_error user deletion logic...")
    
    # Create a user to be deleted
    user = User.objects.create_user(username='test_handle_error_user', password='password')
    user_id = user.id
    print(f"Created user with ID: {user_id}")
    
    # Mock request
    factory = RequestFactory()
    request = factory.get('/')
    
    # Add session
    middleware = SessionMiddleware(lambda x: None)
    middleware.process_request(request)
    request.session.save()
    
    # Add messages
    msg_middleware = MessageMiddleware(lambda x: None)
    msg_middleware.process_request(request)
    
    # Put user_id in session
    request.session['created_user_id'] = user_id
    request.session.save()
    
    print("Calling handle_error...")
    # This should:
    # 1. Pop user_id from session
    # 2. Call django_logout (which would flush session, but we mocked/setup session)
    # 3. Retrieve and delete user
    
    # Note: django_logout requires a user attribute on request usually, so we might need to add it
    request.user = user 
    
    # We really just want to check our logic flow. 
    # django_logout in 'handle_error' will try to flush session.
    
    try:
        handle_error(request, "Error message", "tag", redirect_view_name='login')
    except Exception as e:
        # redirect might cause some issue if not full setup, but we care about user deletion
        # handle_error returns a redirect object, which is fine
        print(f"handle_error returned or raised: {type(e)}")
        pass
        
    # Check if user is deleted
    try:
        u = User.objects.get(id=user_id)
        print("FAIL: User still exists!")
    except User.DoesNotExist:
        print("SUCCESS: User was deleted.")
    except Exception as e:
        print(f"Error checking user: {e}")

if __name__ == '__main__':
    test_handle_error_user_deletion()
