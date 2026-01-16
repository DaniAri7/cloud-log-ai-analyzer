# 1. Usa un'immagine leggera di Python (Cloud-native practice)
FROM python:3.11-slim

# 2. Imposta la cartella di lavoro dentro il container
WORKDIR /app

# 3. Copia solo il file dei requisiti per sfruttare la cache di Docker
COPY requirements.txt .

# 4. Installa le librerie (senza usare la cache di pip per ridurre il peso)
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copia tutto il resto del codice
COPY . .

# 6. Comando per avviare l'analizzatore
CMD ["python", "analyzer.py"]