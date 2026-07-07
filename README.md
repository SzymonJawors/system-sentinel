# System Sentinel v1.0

A lightweight system monitoring security tool written in Python. It audits running processes for high CPU usage, monitors network interfaces for suspicious listening ports, and watches its own source code for tampering.

## Features
- **Integrity Shield (SHA-256)**: On startup, the tool calculates a cryptographic baseline hash of its own source file and continuously re-checks it during runtime, logging a warning if the file has been modified.
- **Process Monitoring**: Scans all active processes every cycle and logs a warning whenever a process exceeds a configurable CPU usage threshold (default: 10%).
- **Network Auditing**: Lists all active listening ports (IPv4/IPv6) and flags potentially malicious activity — e.g. traffic on port `4444`, commonly associated with reverse shells.
- **Triple-Logger System**: Separates output into three independent log files for cleaner auditing:
  - `processes.log` — process/CPU audit results
  - `network.log` — listening ports and network alerts
  - `security.log` — integrity checks and file-tampering alerts
- **Containerized Deployment**: Ships with a `Dockerfile` for easy, isolated deployment.
- **Graceful Shutdown**: Handles `Ctrl+C` (KeyboardInterrupt) cleanly, shutting down without leaving processes hanging.

## Tech Stack
- **Language**: Python 3.x
- **Infrastructure**: Docker
- **Libraries**: `psutil` (cross-platform system/process/network info), `hashlib` (SHA-256 integrity hashing), `logging` (multi-file logging)

## How It Works
On each scan cycle (every 10 seconds), Sentinel:
1. Recomputes the SHA-256 hash of `sentinel.py` and compares it to the initial baseline hash captured at startup.
2. Iterates over all running processes and reports any exceeding the CPU threshold.
3. Iterates over all active network connections and reports listening ports, flagging port `4444` as a critical alert.
4. Sleeps for 10 seconds, then repeats — until interrupted with `Ctrl+C`.

## Installation & Usage

### Run locally
```bash
git clone <repository-url>
cd system-sentinel
pip install -r requirements.txt
python sentinel.py
```

### Run with Docker
```bash
docker build -t system-sentinel .
docker run --rm -it system-sentinel
```

> **Note:** Process and network visibility inside a container is limited to the container's own namespace by default. To monitor the host system, run with elevated privileges/host networking (e.g. `--pid=host --network=host`), and be aware of the security implications of doing so.

## Project Structure
```
system-sentinel/
├── sentinel.py         # Main monitoring script
├── requirements.txt    # Python dependencies (psutil)
├── Dockerfile           # Container build definition
├── .dockerignore
├── .gitignore
└── README.md
```

## Log Files
Running the tool generates three log files in the working directory:

| File | Contents |
|---|---|
| `processes.log` | Timestamped process audits and high-CPU warnings |
| `network.log` | Listening ports found and suspicious-port alerts |
| `security.log` | Startup hash, and warnings if the script's own code changes |

---

# System Sentinel v1.0 (PL)

Lekkie narzędzie bezpieczeństwa do monitorowania systemu, napisane w Pythonie. Sprawdza uruchomione procesy pod kątem wysokiego zużycia CPU, monitoruje interfejsy sieciowe w poszukiwaniu podejrzanych nasłuchujących portów oraz pilnuje integralności własnego kodu źródłowego.

## Funkcje
- **Integrity Shield (SHA-256)**: Przy starcie narzędzie oblicza kryptograficzny hash bazowy własnego pliku źródłowego i na bieżąco go weryfikuje, zapisując ostrzeżenie w logu, jeśli plik zostanie zmodyfikowany.
- **Monitorowanie procesów**: W każdym cyklu skanuje wszystkie aktywne procesy i zapisuje ostrzeżenie, gdy proces przekroczy skonfigurowany próg zużycia CPU (domyślnie 10%).
- **Audyt sieci**: Wyświetla wszystkie aktywne nasłuchujące porty (IPv4/IPv6) i oznacza potencjalnie złośliwą aktywność — np. ruch na porcie `4444`, często kojarzonym z reverse shellami.
- **System potrójnego logowania**: Rozdziela wyniki na trzy niezależne pliki logów, co ułatwia audyt:
  - `processes.log` — wyniki audytu procesów/CPU
  - `network.log` — nasłuchujące porty i alerty sieciowe
  - `security.log` — kontrole integralności i alerty o modyfikacji pliku
- **Wdrożenie w kontenerze**: Zawiera gotowy `Dockerfile` do łatwego, izolowanego wdrożenia.
- **Bezpieczne zamykanie**: Obsługuje `Ctrl+C` (KeyboardInterrupt) i kończy działanie w sposób czysty, bez pozostawiania zawieszonych procesów.

## Stos technologiczny
- **Język**: Python 3.x
- **Infrastruktura**: Docker
- **Biblioteki**: `psutil` (informacje o systemie/procesach/sieci niezależne od platformy), `hashlib` (hashowanie SHA-256 do kontroli integralności), `logging` (logowanie do wielu plików)

## Jak to działa
W każdym cyklu skanowania (co 10 sekund) Sentinel:
1. Ponownie oblicza hash SHA-256 pliku `sentinel.py` i porównuje go z hashem bazowym zapisanym przy starcie.
2. Przechodzi po wszystkich uruchomionych procesach i raportuje te, które przekraczają próg CPU.
3. Przechodzi po wszystkich aktywnych połączeniach sieciowych, raportując nasłuchujące porty i oznaczając port `4444` jako alert krytyczny.
4. Odczekuje 10 sekund i powtarza cykl — aż do przerwania kombinacją `Ctrl+C`.

## Instalacja i użycie

### Uruchomienie lokalne
```bash
git clone <adres-repozytorium>
cd system-sentinel
pip install -r requirements.txt
python sentinel.py
```

### Uruchomienie w Dockerze
```bash
docker build -t system-sentinel .
docker run --rm -it system-sentinel
```

> **Uwaga:** Domyślnie widoczność procesów i sieci wewnątrz kontenera jest ograniczona do przestrzeni nazw samego kontenera. Aby monitorować system hosta, uruchom z podniesionymi uprawnieniami/siecią hosta (np. `--pid=host --network=host`), mając na uwadze związane z tym implikacje bezpieczeństwa.

## Struktura projektu
```
system-sentinel/
├── sentinel.py         # Główny skrypt monitorujący
├── requirements.txt    # Zależności Pythona (psutil)
├── Dockerfile           # Definicja obrazu kontenera
├── .dockerignore
├── .gitignore
└── README.md
```

## Pliki logów
Uruchomienie narzędzia generuje trzy pliki logów w katalogu roboczym:

| Plik | Zawartość |
|---|---|
| `processes.log` | Audyty procesów z sygnaturą czasową i ostrzeżenia o wysokim CPU |
| `network.log` | Znalezione nasłuchujące porty i alerty o podejrzanych portach |
| `security.log` | Hash startowy oraz ostrzeżenia o zmianach we własnym kodzie skryptu |
