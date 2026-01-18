# serial_service/serial_service.py
import serial
import requests
import time

PUERTO = "COM3"      # Ajusta según tu Arduino
BAUDIOS = 9600

API_URL = "http://127.0.0.1:8000/api/rfid/validate/"

ser = serial.Serial(PUERTO, BAUDIOS, timeout=1)
time.sleep(2)

print("[+] Servicio Serial iniciado")

while True:
    uid = ser.readline().decode().strip()
    if not uid:
        continue

    try:
        response = requests.post(API_URL, json={"uid": uid}, timeout=3)
        data = response.json()
        print(f"[API] {data}")

        if response.status_code == 200:
            ser.write(f"OK:{data['message']}\n".encode())
        else:
            ser.write(f"DENY:{data['message']}\n".encode())

    except Exception as e:
        print(f"[ERROR] {e}")
        ser.write(b"DENY:Error\n")
