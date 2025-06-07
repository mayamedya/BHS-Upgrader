import os
import time
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

# SSL doğrulamasız versiyon alma
if not os.getenv('VERSION'):
    try:
        version = r.get("https://panel.buhikayesenin.com/api/version.php", verify=False).text.strip()[0:5]
        os.system(f'git clone https://github.com/mayamedya/BHS-Worker.git ./versions/{version}')
        os.environ['VERSION'] = version
        dotenv.set_key(dotenv.find_dotenv(), "VERSION", version)
    except Exception as e:
        print(f"❌ VERSION alınamadı: {e}")
        version = None

else:
    version = os.getenv('VERSION')

# DEVICEID oluştur
if not os.getenv('DEVICEID'):
    temp_id = generateKey(16, 8)
    dotenv.set_key(dotenv.find_dotenv(), "DEVICEID", temp_id)
    exit(0)

# DEVICEKEY oluştur ve panele gönder
if not os.getenv('DEVICEKEY'):
    temp_key = generateKey(16, 8)
    dotenv.set_key(dotenv.find_dotenv(), "DEVICEKEY", temp_key)
    payload = {
        "device_id": os.getenv("DEVICEID"),
        "device_key": temp_key
    }
    try:
        response = r.post("https://panel.buhikayesenin.com/devices.php", data=payload, verify=False)
        print("🛰️ Cihaz başarıyla gönderildi! Yanıt:", response.text)
    except Exception as e:
        print("🚨 Panel'e gönderim hatası:", e)
    exit(0)

# requirements.txt yükle
if version:
    try:
        os.system(f'pip install -r {os.getcwd()}/versions/{version}/requirements.txt')
    except Exception:
        print("⚠️ requirements.txt yüklenemedi.")

    # worker başlat
    try:
        app = subprocess.Popen(["python3", f"{os.getcwd()}/versions/{version}/main.py"])
    except Exception as e:
        print("🚫 Worker başlatılamadı:", e)
        app = None
else:
    print("❗ VERSION bulunamadı, işlem durduruldu.")
    exit(1)

time.sleep(15)
os.environ['ANYDESK'] = "1"
dotenv.set_key(dotenv.find_dotenv(), "ANYDESK", "1")

# Sonsuz döngü
while True:
    try:
        if app and app.poll() is not None:
            app.terminate()
            app = subprocess.Popen(["python3", f"{os.getcwd()}/versions/{version}/main.py"])

        # Versiyon güncellemesi kontrolü
        try:
            new_version = r.get("https://panel.buhikayesenin.com/api/version.php", verify=False).text.strip()[0:5]
            if new_version != version:
                print("🔄 Yeni versiyon bulundu, güncelleniyor...")
                app.terminate()
                os.system(f'git clone https://github.com/mayamedya/BHS-Worker.git ./versions/{new_version}')
                os.system(f'pip install -r {os.getcwd()}/versions/{new_version}/requirements.txt')
                version = new_version
                dotenv.set_key(dotenv.find_dotenv(), "VERSION", version)
                app = subprocess.Popen(["python3", f"{os.getcwd()}/versions/{version}/main.py"])
        except Exception:
            print("🌐 Güncelleme kontrolü başarısız.")
        sleep(10)
    except Exception as loop_error:
        print("🔁 Döngü hatası:", loop_error)
        sleep(10)
