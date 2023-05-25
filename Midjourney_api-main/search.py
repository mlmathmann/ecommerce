import json
import subprocess
import os
import time
import shutil

#Hier werden die Prompts zusammen gesetzt
#Hier muss der Request der Website rein und verarbeitet werden format des jsons ist momentan noch ausschlaggebend für
#für die generierung
def prompt_extractor():
    json_data = '''
        {
            "style": "fantasy",
            "objekt": "chair",
            "material": "crystal"
        }
        '''

    data = json.loads(json_data)

    prompt = " ".join(data.values())
    print(prompt)

    return prompt


def prompt_sender_reciever(prompt):

    #dieser command erweitert den command für für das skript mit den prompts
    promptcommand = "python3 sender.py --params sender_params.json --prompt " + prompt

    print(promptcommand)

    #hier wird der command mit den prompts ausgeführt
    #subprocess.run(['python3', 'sender.py', '--params', 'sender_params.json', '--prompt', prompt])

    #warte zeit für die generierung
    time.sleep(60)

    return prompt


#def download():

    #command für das downloaden der generierten bilder
    #subprocess.Popen(['python3', 'receiver.py', '--params', 'sender_params.json', '--local_path', 'download'])

#filterfunktion der bilder anhand des namens
#bilder werden momentan in einen anderen ordner nach dem generieren verschoben um funktion zu testen
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


generated_prompt = prompt_extractor()

send_prompts_and_download_image = prompt_sender_reciever(generated_prompt)

print(send_prompts_and_download_image)

download()

image_name = send_prompts_and_download_image

similar_image = find_similar_image_by_name(image_name)
