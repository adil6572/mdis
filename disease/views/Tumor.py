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

model = load_model("ML Models/brain_tumor.h5", compile=False)

def convert_to_pil_image(uploaded_file):
    # Read the content of the uploaded file into a BytesIO buffer
    buffer = BytesIO()
    for chunk in uploaded_file.chunks():
        buffer.write(chunk)
    buffer.seek(0)

    # Create a PIL image from the buffer
    pil_image = Image.open(buffer)

    return pil_image


TUMOR_FAQS={
    "What is the purpose of the Brain Tumor Detection CNN Model?":
        "The Brain Tumor Detection CNN Model is designed to assist in the swift and accurate identification of brain tumors in medical brain scan images. It provides valuable support to healthcare professionals in making informed diagnostic decisions.",

    "How does the model work?":
        "This model utilizes Convolutional Neural Networks (CNNs) to analyze brain scan images. It has been meticulously trained on a diverse dataset of labeled images, enabling it to learn intricate patterns and features associated with brain tumors. When provided with a brain scan image, it generates a prediction regarding the presence or absence of a brain tumor.",

    "What is the accuracy of the Brain Tumor Detection CNN Model?":
        "The current accuracy of this model stands at 94%, based on extensive training with a dataset comprising 20,000 brain scan images.",

    "What types of brain scans are compatible with the model?":
        "The Brain Tumor Detection Model is compatible with various types of brain scans, including MRI (Magnetic Resonance Imaging) and CT (Computed Tomography) scans. It can effectively analyze images acquired through these common imaging modalities for brain tumor detection.",

    "Is the model capable of detecting different types of brain tumors?":
        "Yes, the model has been trained to detect various types of brain tumors, including gliomas, meningiomas, and metastatic tumors, among others. It can provide insights into the presence of different tumor types based on the characteristics observed in the input brain scan.",

    "How can healthcare professionals access and utilize this model for diagnosis?":
        "Healthcare professionals can access the model through our platform or API. They can upload brain scan images, and the model will provide rapid assessments to assist in the diagnosis process. We also offer integration support for seamless incorporation into existing healthcare systems.",

    "Is the model continually updated with new medical research and findings?":
        "Yes, we prioritize staying current with the latest medical knowledge and research findings. Our model is regularly updated with new data and insights, ensuring its effectiveness in line with evolving medical standards and practices."
}


def brain_tumor(request):
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
            img = img.resize((150, 150))
            img_array = np.array(img)
            img_array = img_array.reshape(1, 150, 150, 3)
            a = model.predict(img_array)
            pred = np.argmax(a)


        except Exception as e:
            print(e.__class__, e.__cause__)
        form = ImageForm(request.POST)

        context = {
            "form": form,
            "prediction": True,
            "result":pred,
            "faqs": TUMOR_FAQS,
            "count":0,
            "image_url": file_url,

        }
        response= render(request, 'Tumor.html',context)
        return response


    else:
        form = ImageForm()
        context={
            "form":form,
            "prediction":False,
            "faqs":TUMOR_FAQS,
        }
        return render(request, 'Tumor.html', context)
