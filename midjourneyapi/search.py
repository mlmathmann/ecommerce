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
    categories = [('Tisch', 'desk'), ('Stuhl', 'chair'), ('Beistelltisch', 'coffee table'), ('Sessel', 'armchair'),
                  ('Kunstobjekt', 'art object')]
    styles = [('ARISTROCRATIC'), 'IMAGINATIVE', 'FUTURISTIC', 'BRUTALISTIC', 'SIMPLISTIC']
    materials = [('Helles Holz', 'birch wood'), ('Dunkles Holz', 'dark wood'), ('Perlmutt', 'nacre'),
                 ('Bernstein', 'amber'), ('Chrom', 'chrome'), ('Kristall', 'crystal'), ('Gold', 'gold'),
                 ('Marmor', 'marble'), ('Porzellan', 'porcelain'), ('Beton', 'concrete'), ('Kaschmir', 'cashmere'),
                 ('Nebel', 'fog'), ('Vulkangestein', 'volcanic stone'), ('Obsidian', 'obsidian')]

    if request.method == 'POST':
        style = request.POST.get('style')
        object = request.POST.get('objekt')
        material = request.POST.get('material')

        for listed_category in categories:
            if object == listed_category[0]:
                object = listed_category[1]

        for listed_style in styles:
            if style == listed_style:
                style = listed_style.lower()

        for listed_material in materials:
            if material == listed_material[0]:
                material = listed_material[1]

        json_data = {
            "style": style,
            "objekt": object,
            "material": material
        }
        print(json_data)
        # generated_prompt = prompt_extractor(None)

        # send_prompts_and_download_image = prompt_sender_reciever(generated_prompt)

        # print(send_prompts_and_download_image)

        # download()

        # image_name = send_prompts_and_download_image

        # similar_image = find_similar_image_by_name(image_name)
        item = GeneratedItem()
        item.user = request.user
        item.image = 'uploads/generated/johnjohn_art_object_made_out_of_nacre_be7e519b-6e66-4d55-9b06-193514d944f1.png'
        item.prompt = json_data
        item.save()

        time.sleep(5)
    return HttpResponse(status=201)


# Hier werden die Prompts zusammen gesetzt
# Hier muss der Request der Website rein und verarbeitet werden format des jsons ist momentan noch ausschlaggebend für
# für die generierung
def prompt_extractor(json_data):
    if json_data is None:
        json_data = '''
            {
                "style": "fantasy",
                "objekt": "desk",
                "material": "crystal"
            }
            '''

    data = json.loads(json_data)

    prompt = " ".join(data.values())
    print(prompt)

    return prompt


def prompt_sender_reciever(prompt):
    # dieser command erweitert den command für für das skript mit den prompts
    promptcommand = "python3 sender.py --params sender_params.json --prompt " + prompt

    print(promptcommand)

    # hier wird der command mit den prompts ausgeführt
    # subprocess.run(['python3', 'sender.py', '--params', 'sender_params.json', '--prompt', prompt])

    # warte zeit für die generierung
    time.sleep(60)

    return prompt


# def download():

# command für das downloaden der generierten bilder
# subprocess.Popen(['python3', 'receiver.py', '--params', 'sender_params.json', '--local_path', 'download'])

# filterfunktion der bilder anhand des namens
# bilder werden momentan in einen anderen ordner nach dem generieren verschoben um funktion zu testen
def find_similar_image_by_name(image_name):
    urspruenglicher_string = image_name
    ergebnis_string = "johnjohn_" + urspruenglicher_string.replace(" ", "_").strip()

    print(ergebnis_string)

    ordner_pfad = "download"  # Geben Sie den Pfad zum Ordner an, in dem sich das Bild befindet
    ziel_ordner_pfad = "test"  # Geben Sie den Pfad zum Zielordner an

    gewuenschter_teil = "johnjohn_" + image_name.replace(" ", "_").strip()

    while True:
        for datei_name in os.listdir(ordner_pfad):
            if gewuenschter_teil in datei_name:
                vollstaendiger_pfad = os.path.join(ordner_pfad, datei_name)
                print("Gefundenes Bild:", vollstaendiger_pfad)
                ziel_pfad = os.path.join(ziel_ordner_pfad, datei_name)
                shutil.move(vollstaendiger_pfad, ziel_pfad)  # Move the file to the destination folder
                print("Bild wurde erfolgreich verschoben:", ziel_pfad)
                return image_name

        time.sleep(10)  # Warte 10 Sekunden, bevor der Ordner erneut überprüft wird
