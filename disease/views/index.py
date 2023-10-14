from django.shortcuts import render

FAQS = {
    " What types of medical imaging data do your models accept?": "Our models are designed to work with specific types of medical imaging data. For pneumonia, we utilize chest X-ray images. Brain tumor diagnosis relies on brain scan images, and malaria classification is based on blood smear images",

    "How were your models trained to make accurate diagnoses?": " Our models were trained using large and diverse datasets of labeled medical images. During training, the models learn to recognize disease-specific patterns and features by adjusting their internal parameters to minimize prediction errors.",

    "How do your models assist medical professionals in the diagnosis process?": "Our models serve as valuable tools for medical professionals by providing automated, rapid, and accurate preliminary assessments. They help in prioritizing cases, reducing the workload, and aiding in early detection.",

    "What are the limitations of your models in medical diagnosis?.": "While our models are highly accurate, they are not a replacement for thorough clinical evaluations by medical experts. They provide valuable assistance but should be used in conjunction with professional medical judgment.",
}

context = {
    "faqs": FAQS,
}


def index(request):
    return render(request, "index.html", context=context)
