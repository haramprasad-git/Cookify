
import os
import django
import sys
import shutil

# Setup Django environment
sys.path.append('/home/hara/Program_Files/Python/Web_Apps/Cookify/Cookify')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Cookify.settings')
django.setup()

from django.contrib.auth.models import User
from cooks.models import Cook

def reproduce():
    print("Creating test user and cook...")
    try:
        user = User.objects.create_user(username='test_delete_user_2', password='password123')
        # Create a dummy profile picture file
        if not os.path.exists('media/profile_pictures'):
            os.makedirs('media/profile_pictures', exist_ok=True)
        
        with open('media/profile_pictures/test_pic.png', 'w') as f:
            f.write("dummy image content")

        cook = Cook.objects.create(
            core_user=user, 
            name='Test Cook 2', 
            profile_picture='profile_pictures/test_pic.png'
        )
        print(f"Created Cook: {cook} with profile_pic: {cook.profile_picture}")
        
        print("Attempting to delete user (which cascades to cook)...")
        # This will trigger the signal
        user.delete()
        print("Deletion successful!")
        
        if os.path.exists('media/profile_pictures/test_pic.png'):
            print("WARNING: File was not deleted! (This might be expected depending on storage config, but no error occurred)")
        else:
            print("File deleted successfully.")
        
    except Exception as e:
        print(f"Caught exception during deletion: {e}")
        import traceback
        traceback.print_exc()
        # Clean up if needed
        try:
            if os.path.exists('media/profile_pictures/test_pic.png'):
                os.remove('media/profile_pictures/test_pic.png')
        except:
            pass

if __name__ == '__main__':
    reproduce()
