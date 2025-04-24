from django.shortcuts import render, redirect, HttpResponse
from .models import GrayscaleImage, AttentionedImage, ResizedImage
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.conf import settings
from django.views import View

import io
import numpy as np
from numpy import asarray
import os
from pathlib import Path
from PIL import Image
import torch
import uuid


MODEL_PATH = os.path.join(settings.BASE_DIR, "DL/model_scripted.pt")
TEMP_ID_TO_CLASS = ['bi-modal', 'acicular', 'lamellae']


model = torch.jit.load(MODEL_PATH)
model.eval()


def resize_image(image, coords=(0, 0, 224, 224)):
    try:
        resized_image = image.crop(coords)
        return resized_image
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def get_prediction_and_attention(image_path): # TODO add returning attention
    image = Image.open(image_path).convert('RGB')
    scaled = asarray(image).astype("float32") / 255.0
    print(scaled.shape)

    with torch.no_grad():
        # resized = resized.to(device)

        a = torch.unsqueeze(torch.tensor(np.moveaxis(scaled, -1, 0)), dim=0)
        print(a.shape)
        predicted_probs = model(a)
        predicted_class = torch.argmax(predicted_probs)
    print(scaled.shape)
    return TEMP_ID_TO_CLASS[predicted_class], (scaled * 255).astype(np.uint8) #attention
    

class Index(View):

    def get(self, request):
        return render(request, "upload_form.html")

    def post(self, request):
        image = request.FILES["greyImage"]
        if not image:
            return HttpResponse("no image")

        # Get the uploaded file
        image_file = request.FILES["greyImage"]

        # Save the grayscale image
        grayscale_image = GrayscaleImage(image=image_file)
        grayscale_image.save()

        # Open the uploaded image with Pillow
        pil_image = Image.open(image_file).convert('RGB')

        # Resize the image
        resized_image = resize_image(pil_image)
        if resized_image is None:
            return HttpResponse("Error resizing image", status=500)

        # Save the resized image to a BytesIO object
        resized_image_io = io.BytesIO()
        resized_image.save(resized_image_io, format="PNG")
        resized_image_file = ContentFile(
            resized_image_io.getvalue(), "resized_image.jpg"
        )

        # Save the resized image to the database
        resized_image_entry = ResizedImage(
            grayscale_image=grayscale_image, image=resized_image_file
        )
        resized_image_entry.save()

        # temperary path
        temp_path = default_storage.save(
            "temp/" + str(uuid.uuid4()) + ".png",
            ContentFile(resized_image_io.getvalue()),
        )

        # call the funtion to convert grey scale image to coloured image
        predicted_class, attentioned_image_np = get_prediction_and_attention(default_storage.path(temp_path))
        attentioned_pil_image = Image.fromarray(attentioned_image_np)
        attentioned_image_io = io.BytesIO()
        attentioned_pil_image.save(attentioned_image_io, format="PNG")
        attentioned_image_file = ContentFile(
            attentioned_image_io.getvalue(), "attentioned_image.png"
        )

        # Save the attentioned image to the database
        attentioned_image_entry = AttentionedImage(
            predicted_class=predicted_class, grayscale_image=grayscale_image, image=attentioned_image_file
        )
        attentioned_image_entry.save()
        response_data = {
            "signature_token": grayscale_image.signature,
            "download_attention_token": attentioned_image_entry.download_token,
            "predicted_class": predicted_class
        }

        return JsonResponse(response_data, status=201)