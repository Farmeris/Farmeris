from PIL import Image

# Create your views here.
def is_valid_image(file):
    #Check if the given file is a valid image.
    try:
        # Open the image file using Pillow
        image = Image.open(file)
        image.verify()  # Verify if it's a valid image
        return True
    except (IOError, PIL.UnidentifiedImageError):
        return False