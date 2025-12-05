import sys
import time
from datetime import datetime
from multiprocessing.managers import BaseManager

PORT = 50002
AUTH_KEY = b"abc"


class ServiceProvider:
    """
    Implementazione dei servizi Greeting e Hour.
    Equivalente a Es2RMIserver.java
    """

    def greeting(self):
        print("[Server] Richiesta Greeting ricevuta")
        return "Hello RMI World from Python!"

    def hour(self):
        print("[Server] Richiesta Hour ricevuta")
        return datetime.now().hour


def start_server():
    BaseManager.register("get_services", callable=lambda: ServiceProvider())
    manager = BaseManager(address=("", PORT), authkey=AUTH_KEY)
    print(f"[Server] Servizi attivi su porta {PORT}...")
    server = manager.get_server()
    server.serve_forever()


def start_client(service_type):
    BaseManager.register("get_services")
    manager = BaseManager(address=("localhost", PORT), authkey=AUTH_KEY)

    try:
        manager.connect()
    except ConnectionRefusedError:
        print("Errore: Server non raggiungibile.")
        return

    remote_obj = manager.get_services()

    if service_type == "greeting":
        print(f"[Client] Greeting ricevuto: {remote_obj.greeting()}")
    elif service_type == "hour":
        print(f"[Client] Ora ricevuta: {remote_obj.hour()}")
    else:
        print("Servizio non riconosciuto. Usa 'greeting' o 'hour'.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python ex2_services.py [server | client <greeting/hour>]")
        sys.exit(1)

    mode = sys.argv[1]

    if mode == "server":
        start_server()
    elif mode == "client":
        srv = sys.argv[2] if len(sys.argv) > 2 else "greeting"
        start_client(srv)
