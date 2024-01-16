from django.shortcuts import render
import os


def doctors_view(request):
    image_folder = 'static/images/profile_images'
    image_paths = [os.path.join(image_folder, filename) for filename in os.listdir(image_folder)]

    return render(request, 'index.html', {'doctor_images': image_paths})