import os
import dotenv
from dotenv import load_dotenv
from time import sleep
import requests as r
import subprocess
# import re

load_dotenv()
if not os.path.exists('./versions/'):
    os.mkdir('./versions/')

if os.getenv('VERSION') == "":
    version = r.get("https://panel.buhikayesenin.com/api/version.php").text.replace('\n', "")
    version = version[0:4]
    os.system('git clone https://github.com/ardayasar/BHS-Worker.git ./versions/' + version)
    os.environ['VERSION'] = version
    dotenv.set_key(dotenv.find_dotenv(), "VERSION", os.environ["VERSION"])

if os.getenv('DEVICEID') == "":
    devIDInput = input("Cihaz ID'si bulunamadı. Size verilen DEVICEID'yi yazar mısınız?: ")
    if len(devIDInput) == 24:
        dotenv.set_key(dotenv.find_dotenv(), "DEVICEID", devIDInput)
    else:
        print("Hata Mesajı: DEVICEID doğru değil")

if os.getenv('AUTHKEY') == "":
    devAUInput = input("Cihaz AUTHKYEY'i bulunamadı. Size verilen AUTHKEY'i yazar mısınız?: ")
    if len(devAUInput) == 24:
        dotenv.set_key(dotenv.find_dotenv(), "AUTHKEY", devAUInput)
    else:
        print("Hata Mesajı: AUTHKEY doğru değil")


os.system('pip install -r ' + os.getcwd() + '/versions/' + os.getenv("VERSION") + '/requirements.txt')
app = subprocess.Popen(["python3", os.getcwd() + "/versions/" + os.getenv('VERSION') + "/main.py"])

while True:
    try:
        version = r.get("https://panel.buhikayesenin.com/api/version.php").text
        # version = version[0:4]
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
