from django.db import models
import uuid

class GrayscaleImage(models.Model):
    image = models.ImageField(upload_to='grayscale_images/')
    signature = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.signature)