import asyncio
import json
import qrcode
import socket
import websockets
from datetime import datetime

# --- CONFIGURATION ---
PORT = 8765

def get_local_ip():
    """Fetches the local IP address of your PC to generate the QR code."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def generate_qr(url):
    """Generates a QR code in the terminal."""
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)
    print("\n--- NEWVIEW API: SCAN TO CONNECT ---")
    qr.print_ascii()
    print(f"URL: {url}\n")

async def security_logger(device_info, raw_data):
    """Forensic logging for unauthorized attempts or validation failures."""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "product_id": device_info.get("product_id", "UNKNOWN"),
        "model": device_info.get("model", "UNKNOWN"),
        "captured_payload": raw_data
    }
    with open("security_forensics.log", "a") as f:
        f.write(json.dumps(log_entry) + "\n")
    print(f"!!! SECURITY LOG GENERATED: {device_info.get('model')} !!!")

async def handler(websocket):
    """Handles incoming data from Games and Mobile Clients."""
    print(f"New connection established.")
    try:
        async for message in websocket:
            data = json.loads(message)
            
            # --- VALIDATION LAYER ---
            if "auth_token" not in data:
                # Trigger forensic log if packet is suspicious
                device_info = data.get("device_info", {})
                await security_logger(device_info, message)
                continue

            # Route data (from Game to Mobile or vice-versa)
            # For now, we just broadcast to all connected clients
            await asyncio.gather(*[client.send(message) for client in connected_clients if client != websocket])

    except websockets.exceptions.ConnectionClosed:
        print("Connection closed.")

connected_clients = set()

async def main():
    local_ip = get_local_ip()
    # Replace with your PWA hosted URL later
    pwa_url = f"http://{local_ip}:5000" 
    generate_qr(pwa_url)

    async with websockets.serve(handler, "0.0.0.0", PORT):
        print(f"NewView Bridge Server running on ws://{local_ip}:{PORT}")
        await asyncio.future() # Run forever

if __name__ == "__main__":
    asyncio.run(main())