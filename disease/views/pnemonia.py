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

model = load_model("ML Models/pneumonia.h5")

def convert_to_pil_image(uploaded_file):
    # Read the content of the uploaded file into a BytesIO buffer
    buffer = BytesIO()
    for chunk in uploaded_file.chunks():
        buffer.write(chunk)
    buffer.seek(0)

    # Create a PIL image from the buffer
    pil_image = Image.open(buffer)

    return pil_image


PNEMONIA_FAQS={
    " What is the purpose of the Pneumonia Model?": "The Pneumonia Model is designed to assist in the automated diagnosis of pneumonia from X-ray images. Its primary purpose is to quickly and accurately identify the presence or absence of pneumonia in a given image.",

    "How does the Pneumonia Model work?":" The Pneumonia Model is based on Convolutional Neural Networks (CNNs), a type of deep learning model. It analyzes features in X-ray images to recognize signs of pneumonia. It has been trained on a dataset of labeled pneumonia and non-pneumonia images to learn disease-related patterns.",

    "What types of X-ray images can be used with the Pneumonia Model?":"TThe Pneumonia Model is designed for chest X-ray images, specifically those used in pneumonia diagnosis. These images focus on the chest area to assess lung health.",

    "Is the Pneumonia Model capable of differentiating between different types of pneumonia (e.g., bacterial, viral)?":"The primary function of the model is to detect the presence of pneumonia, not to differentiate between pneumonia types. It identifies the overall presence of the condition.",

    "Does the Pneumonia Model replace the need for radiologists or physicians in pneumonia diagnosis?":"No, the Pneumonia Model is designed to support healthcare professionals but does not replace the expertise of radiologists or physicians. It can assist in the initial screening process, but the final diagnosis and treatment decisions should still involve medical experts."


}

def pnemonia_view(request):
    if request.method == 'POST':
        uploaded_image = request.FILES.get('image')


        print(type(uploaded_image))


        if uploaded_image:
            random_filename = str(uuid.uuid4())
            file_extension = os.path.splitext(uploaded_image.name)[1]
            filename = random_filename + file_extension
            file_path = default_storage.save(f'media/{filename}', uploaded_image)
            file_url = f'{settings.MEDIA_URL}{file_path}'
            pil_image = convert_to_pil_image(uploaded_image)


        try:
            img = pil_image
            img = img.resize((36, 36))
            img = np.asarray(img)
            img = img.reshape((1, 36, 36, 1))
            img = img / 255.0
            pred = np.argmax(model.predict(img)[0])
            print(img)
            print(pred)
        except Exception as e:
            print(e.__class__, e.__cause__)
        form = ImageForm(request.POST)

        context = {
            "form": form,
            "prediction": True,
            "Result":pred,
            "faqs": PNEMONIA_FAQS,
            "count":0,
            "image_url": file_url,

        }
        return render(request, 'pnemonia.html',context)

    else:
        form = ImageForm()
        context={
            "form":form,
            "prediction":False,
            "faqs":PNEMONIA_FAQS,
        }
        return render(request, 'pnemonia.html', context)
