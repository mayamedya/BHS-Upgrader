import os
import dotenv
from dotenv import load_dotenv
from time import sleep
import requests as r
import subprocess
import string
import random

def generateKey(letters_count, digits_count):
    letters = ''.join((random.choice(string.ascii_letters) for i in range(letters_count)))
    digits = ''.join((random.choice(string.digits) for i in range(digits_count)))
    sample_list = list(letters + digits)
    random.shuffle(sample_list)
    final_string = ''.join(sample_list)
    return final_string


load_dotenv()
if not os.path.exists('./versions/'):
    os.mkdir('./versions/')

if os.getenv('VERSION') == "":
    version = r.get("https://panel.buhikayesenin.com/api/version.php").text
    version = version[0:4]
    os.system('git clone https://github.com/ardayasar/BHS-Worker.git ./versions/' + version)
    os.environ['VERSION'] = version
    dotenv.set_key(dotenv.find_dotenv(), "VERSION", os.environ["VERSION"])

if os.getenv('DEVICEID') == "":
    temp_id = generateKey(16, 8)
    dotenv.set_key(dotenv.find_dotenv(), "DEVICEID", temp_id)

if os.getenv('AUTHKEY') == "":
    temp_key = generateKey(16, 8)
    dotenv.set_key(dotenv.find_dotenv(), "AUTHKEY", temp_key)


os.system('pip install -r ' + os.getcwd() + '/versions/' + os.getenv("VERSION") + '/requirements.txt')
app = subprocess.Popen(["python3", os.getcwd() + "/versions/" + os.getenv('VERSION') + "/main.py"])

while True:
    try:
        version = r.get("https://panel.buhikayesenin.com/api/version.php").text
        version = version[0:4]
        if version != os.getenv('VERSION'):
            print('New version found! Downloading...')
            app.terminate()
            try:
                os.system('git clone https://github.com/ardayasar/BHS-Worker.git ' + os.getcwd() + '/versions/' + version)
            except Exception as e:
                print('Error while downloading version')
                quit()
            os.environ['VERSION'] = version
            dotenv.set_key(dotenv.find_dotenv(), "VERSION", os.environ["VERSION"])
            os.system('pip install -r ' + os.getcwd() + '/versions/' + os.getenv("VERSION") + '/requirements.txt')
            app = subprocess.Popen(["python3", os.getcwd() + "/versions/" + os.getenv('VERSION') + "/main.py"])
        sleep(10)
    except:
        print('Error')
