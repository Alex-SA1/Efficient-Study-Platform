from PIL import Image
from django.core.exceptions import ValidationError
import os


def validate_image(file):
    """
    method that checks if a given file is a valid image
    """
    try:
        file_frame = file.tell()  # saving the first frame of the file

        image = Image.open(file)
        image.verify()

        # reset to the first frame of the file
        file.seek(file_frame)

    except Exception:
        raise ValidationError("The uploaded file is not a valid image")


def validate_image_size(file):
    """
    method that checks if the size of the file is less than 2mb
    """
    mb_size = 1024 * 1024  # size of a mb in bytes
    max_size = 2 * mb_size

    if file.size > max_size:
        raise ValidationError("The uploaded file is bigger than 2mb")
