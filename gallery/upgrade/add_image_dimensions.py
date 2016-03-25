#Updates 10 images records at a time and saves the height and width into the db

from gallery.models import Image

print("Start")

images = Image.objects.filter(original_image_height__isnull=True)[:10]

for image in images:
    image.save()
