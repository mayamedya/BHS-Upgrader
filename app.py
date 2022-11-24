import os
import dotenv
from dotenv import load_dotenv
from time import sleep
import requests as r
import subprocess

load_dotenv()
if not os.path.exists('./versions/'):
    os.mkdir('./versions/')

if os.getenv('VERSION') == "":
    version = r.get("https://panel.buhikayesenin.com/api/version.php").text[0:4]
    os.system('git clone https://github.com/ardayasar/BHS-Worker.git ./versions/' + version)
    os.environ['VERSION'] = version
    dotenv.set_key(dotenv.find_dotenv(), "VERSION", os.environ["VERSION"])

app = subprocess.Popen(["python3", os.getcwd() + "/versions/" + os.getenv('VERSION') + "/main.py"])

while True:
    try:
        version = r.get("https://panel.buhikayesenin.com/api/version.php").text[0:4]
        if version != os.getenv('VERSION'):
            print('New version found! Downloading...')
            app.terminate()
            try:
                os.system('git clone https://github.com/ardayasar/BHS-Worker.git ./versions/' + version)
            except Exception as e:
                print('Error while downloading version')
                quit()
            os.environ['VERSION'] = version
            dotenv.set_key(dotenv.find_dotenv(), "VERSION", os.environ["VERSION"])
            app = subprocess.Popen(["python3", os.getcwd() + "/versions/" + os.getenv('VERSION') + "/main.py"])
        sleep(10)
    except:
        print('Error')
