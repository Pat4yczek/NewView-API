import asyncio
import websockets
import json
import qrcode
import socket
from datetime import datetime

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 1))
        ip = s.getsockname()[0]
    except Exception: ip = '127.0.0.1'
    finally: s.close()
    return ip

async def handler(websocket):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Połączono z urządzeniem.")
    try:
        async for message in websocket:
            data = json.loads(message)
            if data['type'] == 'DATA':
                # Wyświetlamy Velocity i Aftertouch w jednej linii (diagnostyka)
                print(f"V: {data['v']:.2f} | A: {data['a']:.2f} | Radius: {data['r']:.1f}", end='\r')
    except Exception as e:
        print(f"\nRozłączono: {e}")

async def main():
    ip = get_local_ip()
    port = 8765
    # Link do Twojego hostingu (może to być localhost jeśli testujesz na tym samym kompie)
    link = f"http://{ip}:8080" 
    
    print("-" * 30)
    print(f"NEWVIEW API SERVER")
    print(f"Twoje IP: {ip}")
    print(f"Skanuj kod, aby otworzyć interfejs:")
    
    qr = qrcode.QRCode(border=2)
    qr.add_data(link)
    qr.print_ascii()
    
    print(f"Czekam na połączenie na porcie {port}...")
    async with websockets.serve(handler, "0.0.0.0", port):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())