from django.db import models
import uuid

class GrayscaleImage(models.Model):
    image = models.ImageField(upload_to='grayscale_images/')
    signature = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.signature)
    
class ResizedImage(models.Model):
    grayscale_image = models.OneToOneField(GrayscaleImage, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='resized_images/')

    def __str__(self):
        return f"Resized image for {self.grayscale_image.signature}"

class AttentionedImage(models.Model):
    grayscale_image = models.OneToOneField(GrayscaleImage, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='attentioned_images/')
    download_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    predicted_class = models.TextField(default="I don’t know")
    # temperature = ...
    # composition = ...

    def __str__(self):
        return str(self.download_token)