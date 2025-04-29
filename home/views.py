from django.shortcuts import render, redirect, HttpResponse
from .models import GrayscaleImage
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.conf import settings
from django.views import View

import io
import numpy as np
from numpy import asarray
import os
from PIL import Image
import torch
import uuid
from torchvision.transforms import v2
import torch
# from sklearn.preprocessing import MinMaxScaler
import joblib


MODEL_PATH = os.path.join(settings.BASE_DIR, "DL/model_scripted.pt")
SCALER_PATH = os.path.join(settings.BASE_DIR, "DL/scaler.gz")

MMScaler = joblib.load(SCALER_PATH)
model = torch.jit.load(MODEL_PATH)
model.eval()


def transform(pic):
    trans = v2.Compose([
        v2.ToImage(),
        v2.ToDtype(torch.float32, scale=True),
        v2.RandomHorizontalFlip(p=0.5),
        v2.RandomVerticalFlip(p=0.5),
        v2.RandomCrop(size=(224, 224)),
    ])
    return trans(pic)

def get_prediction(image):
    batch = []
    for _ in range(10):
        batch.append(transform(image))
    batch_tensor = torch.stack(batch)

    with torch.no_grad():
        predicted_concentration = model(batch_tensor)
    return torch.tensor(MMScaler.inverse_transform(predicted_concentration.reshape(-1, 1))).mean().item()
    

class Index(View):

    def get(self, request):
        return render(request, "upload_form.html")

    def post(self, request):
        image = request.FILES["greyImage"]
        if not image:
            return HttpResponse("no image")

        # Get the uploaded file
        image_file = request.FILES["greyImage"]

        # Open the uploaded image with Pillow
        pil_image = Image.open(image_file).convert('RGB')

        if pil_image.size[0] < 224 or pil_image.size[1] < 224:
            return HttpResponse("Too small image")
        if pil_image.size[0] > 1000 or pil_image.size[1] > 1000:
            return HttpResponse("Too big image")

        # Save the grayscale image
        grayscale_image = GrayscaleImage(image=image_file)
        grayscale_image.save()

        # call the funtion to convert grey scale image to coloured image
        predicted_Fe_concentration = get_prediction(pil_image)

        response_data = {
            "signature_token": grayscale_image.signature,
            "predicted_Fe_concentration": predicted_Fe_concentration
        }

        return JsonResponse(response_data, status=201)