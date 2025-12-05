import sys
import os
from multiprocessing.managers import BaseManager

PORT = 50003
AUTH_KEY = b"abc"
CHUNK_SIZE = 4096  # Leggiamo 4KB alla volta, NON 1 byte!


class OptimizedFileReader:
    """
    Correzione Logica rispetto alle slide Java:
    1. Usa 'rb' (Read Binary) invece di FileOutputStream (che scriveva/distruggeva).
    2. Implementa lettura a 'chunk' per evitare l'overhead di rete byte-per-byte.
    3. Gestisce apertura e chiusura file con 'with' (Context Manager) per evitare leak.
    """

    def read_chunk(self, filename, offset):
        """
        Legge un blocco di dati dal file a partire da 'offset'.
        Ritorna bytes o None se EOF.
        """
        if not os.path.exists(filename):
            print(f"[Server] File non trovato: {filename}")
            raise FileNotFoundError(f"Il file {filename} non esiste sul server.")

        print(f"[Server] Lettura '{filename}' offset {offset}")

        try:
            # CORREZIONE 1 e 2: Uso 'rb' e context manager
            with open(filename, "rb") as f:
                f.seek(offset)
                data = f.read(CHUNK_SIZE)  # Legge 4KB

            # Se data è vuoto, siamo a EOF
            if not data:
                return None
            return data

        except Exception as e:
            print(f"[Server] Errore I/O: {e}")
            raise e


def start_server():
    BaseManager.register("get_reader", callable=lambda: OptimizedFileReader())
    manager = BaseManager(address=("", PORT), authkey=AUTH_KEY)
    print(f"[Server] File Reader attivo su porta {PORT}...")
    server = manager.get_server()
    server.serve_forever()


def start_client(remote_filename, local_filename):
    BaseManager.register("get_reader")
    manager = BaseManager(address=("localhost", PORT), authkey=AUTH_KEY)

    try:
        manager.connect()
    except ConnectionRefusedError:
        print("Errore: Server non raggiungibile.")
        return

    reader = manager.get_reader()

    print(
        f"[Client] Inizio download di '{remote_filename}' verso '{local_filename}'..."
    )

    offset = 0
    total_bytes = 0

    try:
        # CORREZIONE 1: Apertura in scrittura binaria ('wb')
        with open(local_filename, "wb") as fw:
            while True:
                # CORREZIONE 3: Richiesta a blocchi, non byte per byte
                chunk = reader.read_chunk(remote_filename, offset)

                if chunk is None:  # EOF
                    break

                fw.write(chunk)

                bytes_read = len(chunk)
                offset += bytes_read
                total_bytes += bytes_read

                # Feedback visuale
                print(f"\rScaricati: {total_bytes} bytes...", end="")

        print(f"\n[Client] Download completato con successo ({total_bytes} bytes).")

    except Exception as e:
        print(f"\n[Client] Errore durante il trasferimento: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Uso: python ex3_4_file_transfer.py [server | client <remote_file> <local_file>]"
        )
        sys.exit(1)

    mode = sys.argv[1]

    if mode == "server":
        start_server()
    elif mode == "client":
        if len(sys.argv) < 4:
            print("Specifica file remoto e file locale.")
        else:
            start_client(sys.argv[2], sys.argv[3])
