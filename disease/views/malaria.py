import os
import uuid

from django.core.files.storage import default_storage
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from io import BytesIO
from django.shortcuts import render
from django.http import HttpResponse
from disease.forms import ImageForm
from keras.models import  load_model
import numpy as np

from mdis import settings

model = load_model("ML Models/malaria.h5")

def convert_to_pil_image(uploaded_file):
    # Read the content of the uploaded file into a BytesIO buffer
    buffer = BytesIO()
    for chunk in uploaded_file.chunks():
        buffer.write(chunk)
    buffer.seek(0)

    # Create a PIL image from the buffer
    pil_image = Image.open(buffer)

    return pil_image


MALARIA_FAQS={
    "What is the purpose of the new Malaria Classification CNN Model?": "The new Malaria Classification CNN Model is designed to automatically and accurately identify the presence or absence of malaria parasites in microscopic blood smear images. It aids in the rapid and efficient diagnosis of malaria, supporting healthcare professionals in making timely treatment decisions.",

    "How does the model work?":"The model uses Convolutional Neural Networks (CNNs) to analyze the visual features of microscopic blood smear images. It has been trained on a dataset of labeled images to learn patterns associated with malaria parasites. When provided with an image, it generates a prediction regarding the presence or absence of malaria",

    "What is the accuracy of the Malaria Classification CNN Model?":"The Currenr accuarcy of this model is 96% which is trained on 27000 images",

    "What kind of images can be used with the Malaria Model?":"The Malaria Model is specifically designed for microscopic blood smear images commonly used in malaria diagnosis. These images are obtained by placing a blood sample on a glass slide and examining it under a microscope.",


}

def malaria(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.cleaned_data['image']
            filename = uploaded_image.name
            print("Image is valid")

        if uploaded_image:
            random_filename = str(uuid.uuid4())
            file_extension = os.path.splitext(uploaded_image.name)[1]
            filename = random_filename + file_extension
            file_path = default_storage.save(f'media/{filename}', uploaded_image)
            file_url = f'{settings.MEDIA_URL}{file_path}'

            # Process the uploaded image
            pil_image = convert_to_pil_image(uploaded_image)

        try:
            img = pil_image
            img = img.resize((36, 36))
            img = np.asarray(img)
            img = img.reshape((1, 36, 36, 3))
            img = img.astype(np.float64)

            pred = np.argmax(model.predict(img)[0])
            print(pred)
        except Exception as e:
            print(e.__class__, e.__cause__)
        form = ImageForm(request.POST)

        context = {
            "form": form,
            "prediction": True,
            "result":pred,
            "faqs": MALARIA_FAQS,
            "count":0,
            "image_url": file_url,

        }
        response= render(request, 'malaria.html',context)
        return response


    else:
        form = ImageForm()
        context={
            "form":form,
            "prediction":False,
            "faqs":MALARIA_FAQS,
        }
        return render(request, 'malaria.html', context)
