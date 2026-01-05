import asyncio
import websockets
import json

# Prosta baza "znanych" urządzeń (Forensic Logging)
trusted_devices = {}

async def new_view_handler(websocket, path):
    print(f"[*] Nowe połączenie: {websocket.remote_address}")
    
    try:
        async for message in websocket:
            data = json.loads(message)
            
            # 1. HANDSHAKE / AUTH
            if data.get("type") == "AUTH":
                device_id = data["uuid"]
                trusted_devices[device_id] = data["meta"]
                print(f"[AUTH] Urządzenie zweryfikowane: {device_id}")
            
            # 2. PRZETWARZANIE AFTERTOUCH / VELOCITY
            elif data.get("type") == "INPUT":
                val = data.get("val", 0)
                # ANTI-TAMPER: Sprawdzamy czy wartość jest w zakresie 0-1
                if 0 <= val <= 1:
                    print(f"[INPUT] Aftertouch: {val:.2f}")
                    # TUTAJ: Wyślij dane do konektora gry
                else:
                    print(f"[ALERT] Wykryto manipulację danymi od {websocket.remote_address}")

    except websockets.exceptions.ConnectionClosedError:
        print("[-] Połączenie przerwane")

start_server = websockets.serve(new_view_handler, "0.0.0.0", 8765)

print("[NV SERVER] Start na porcie 8765...")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()