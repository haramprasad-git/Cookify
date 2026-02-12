from django.core.exceptions import ValidationError
from PIL import Image

def validate_image_type(file):
    '''Allow image files only'''
    try:
        with Image.open(file.path) as img:
            img.verify()
    except Exception as e:
        print(e)
        raise ValidationError('Invalid Image File')

def validate_file_size(file):
    '''Allow only images under 5MB'''
    max_size = 5 * 1024 * 1024
    if file.size > max_size:
        raise ValidationError('Use Images under 5MB')