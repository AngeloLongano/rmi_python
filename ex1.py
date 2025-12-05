import sys
import time
from multiprocessing.managers import BaseManager

# --- Configurazione RMI ---
PORT = 50001
AUTH_KEY = b"abc"  # Password di sicurezza (obbligatoria in Python managers)


class StringReverser:
    """
    Classe che implementa la logica di business (Server Side).
    Equivalente a Es1RMIserver.java
    """

    def overturn(self, s):
        print(f"[Server] Ricevuta richiesta di overturn per: '{s}'")
        # In Python le stringhe si invertono con lo slicing [::-1]
        return s[::-1]


def start_server():
    """Avvia il server RMI"""
    # 1. Registriamo la classe nel manager
    BaseManager.register("get_reverser", callable=lambda: StringReverser())

    # 2. Configuriamo la connessione
    manager = BaseManager(address=("", PORT), authkey=AUTH_KEY)

    print(f"[Server] In ascolto sulla porta {PORT}...")
    server = manager.get_server()
    server.serve_forever()


def start_client(message):
    """Avvia il client RMI"""
    # 1. Registriamo l'interfaccia (stesso nome usato dal server)
    BaseManager.register("get_reverser")

    # 2. Connettiamo al server
    manager = BaseManager(address=("localhost", PORT), authkey=AUTH_KEY)
    try:
        manager.connect()
    except ConnectionRefusedError:
        print("Errore: Impossibile connettersi. Il server è avviato?")
        return

    # 3. Otteniamo l'oggetto remoto (Stub)
    reverser = manager.get_reverser()

    # 4. Chiamata remota
    try:
        result = reverser.overturn(message)
        print(f"[Client] Messaggio inviato: '{message}'")
        print(f"[Client] Risultato ricevuto: '{result}'")
    except Exception as e:
        print(f"Errore durante la chiamata RMI: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python ex1_reverse.py [server | client <messaggio>]")
        sys.exit(1)

    mode = sys.argv[1]

    if mode == "server":
        start_server()
    elif mode == "client":
        msg = sys.argv[2] if len(sys.argv) > 2 else "Test RMI"
        start_client(msg)
    else:
        print("Modalità non riconosciuta.")
