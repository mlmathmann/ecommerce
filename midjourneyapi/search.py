import json
import subprocess
import os
import time
import shutil

from django.shortcuts import redirect, render
from store.models import GeneratedItem
from store.views import get_navbar_context
from django.contrib import messages
from django.http import HttpResponse


def creation(request):

    style = request.POST.get('style')
    object = request.POST.get('objekt')
    material = request.POST.get('material')

    json_data = {
        "style": style.lower(),
        "objekt": object.lower(),
        "material": material.lower()
    }

    website_json = prompt_extractor(json_data)

    send_prompts_to_discord = prompt_sender(website_json)

    download_created_image()

    image_name = send_prompts_to_discord

    image_in_folder = find_image_in_folder(image_name)
    print("Result : ", image_in_folder)

    item = GeneratedItem()
    item.user = request.user
    item.image = image_in_folder
    item.prompt = json_data
    item.save()

    return HttpResponse(status=201)


def prompt_extractor(json_data):
    prompt = " ".join(json_data.values())
    print(prompt)

    return prompt


def prompt_sender(prompt):
    promptcommand = "python3 midjourneyapi/sender.py --params midjourneyapi/sender_params.json --prompt " + prompt

    print(promptcommand)

    subprocess.run(
        ['python3', 'midjourneyapi/sender.py', '--params', 'midjourneyapi/sender_params.json', '--prompt', prompt])

    return prompt


def download_created_image():
    subprocess.Popen(
        ['python3', 'midjourneyapi/receiver.py', '--params', 'midjourneyapi/sender_params.json', '--local_path',
         'static/uploads'],)


def find_image_in_folder(prompt):
    time.sleep(5)
    print("60 sek sind over")
    print(prompt)
    full_image_name = "johnjohn_" + prompt.replace(" ", "_").strip()

    print(full_image_name)
    print(prompt)

    file_path = "static/uploads"

    full_image_name = "johnjohn_" + prompt.replace(" ", "_").strip()

    while True:

        for file_name in os.listdir(file_path):

            if full_image_name in file_name:

                vollstaendiger_pfad = os.path.join("uploads", file_name)

                print(vollstaendiger_pfad)

                return vollstaendiger_pfad

        time.sleep(10)