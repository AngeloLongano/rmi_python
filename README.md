# Esercizi RMI in Python

Questo progetto contiene una serie di script Python che replicano e migliorano alcuni esercizi originariamente sviluppati in Java RMI.

L'obiettivo è dimostrare i concetti di base dell'invocazione di metodi a distanza (Remote Method Invocation) utilizzando esclusivamente la libreria standard di Python `multiprocessing.managers`.

## Come Eseguire gli Script

Ogni file `ex*.py` è auto-contenuto e implementa sia la logica del **Server** che quella del **Client**. Per eseguire un esercizio, sono necessari **due terminali separati**.

1. In un terminale, avvia il **Server**.
2. Nel secondo terminale, avvia il **Client** con i parametri richiesti.

---

### 📝 Esercizio 1: `ex1.py` - Reverse di una Stringa

Questo esercizio implementa un semplice servizio remoto che inverte una stringa ricevuta dal client.

**Terminale 1: Server**

```bash
python ex1.py server
```

**Terminale 2: Client**

```bash
python ex1.py client "La mia stringa di prova"
```

---

### 🕒 Esercizio 2: `ex2.py` - Servizi Multipli (Greeting & Ora)

Il server espone due metodi remoti: uno che restituisce un messaggio di saluto e un altro che restituisce l'ora corrente.

**Terminale 1: Server**

```bash
python ex2.py server
```

**Terminale 2: Client**

```bash
# Per il servizio di saluto
python ex2.py client greeting

# Per conoscere l'ora
python ex2.py client hour
```

---

### 📂 Esercizio 3 & 4: `ex3_4.py` - Trasferimento File Ottimizzato

Questo script implementa un servizio di trasferimento file che corregge un'inefficienza comune: invece di trasferire il file un byte alla volta, lo invia in "blocchi" (chunk), migliorando drasticamente le performance.

**Setup (Crea un file di prova)**

```bash
echo "Questo è un file di testo di prova per il trasferimento remoto." > prova.txt
```

**Terminale 1: Server**

```bash
python ex3_4.py server
```

**Terminale 2: Client**

```bash
# Scarica 'prova.txt' dal server e lo salva come 'scaricato.txt'
python ex3_4.py client prova.txt scaricato.txt
```
