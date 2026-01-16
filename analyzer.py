import os
import pandas as pd
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# 1. Caricamento variabili d'ambiente (Security First)
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Definizione della "Allowlist" degli IP autorizzati
AUTHORIZED_IPS = ["192.168.1.10", "10.0.0.50", "172.16.0.5"]

def load_and_filter_logs(filepath): #analizza i log di AWS CloudTrail
    """Carica i log AWS e applica filtri di sicurezza avanzati usando Pandas."""
    try: 
        df = pd.read_json(filepath) # Legge il file JSON e lo converte in un DataFrame Pandas
        if df.empty:
            return pd.DataFrame() 
        
        # CONDIZIONE A: Il login è fallito (verifica nel dizionario nidificato)
        login_failed = df['responseElements'].apply(
            lambda x: x.get('ConsoleLogin') == 'Failure' if isinstance(x, dict) else False
        ) # isinstance(x, dict): Controlla se la cella contiene un dizionario (oggetto JSON). x.get('ConsoleLogin') == 'Failure': Se è un dizionario, cerca la chiave "ConsoleLogin" e verifica se il valore è "Failure". else False: Se la cella è vuota o non è un dizionario, scarta la riga 

        # CONDIZIONE B: L'IP di origine non è tra quelli conosciuti (Zero Trust)
        unauthorized_ip = ~df['sourceIPAddress'].isin(AUTHORIZED_IPS)  

        # Filtro finale: Segnaliamo se A oppure B è vera (| è l'operatore OR in Pandas)
        suspicious_df = df[login_failed | unauthorized_ip].copy()
        
        return suspicious_df
    except Exception as e:
        print(f"❌ Errore durante l'elaborazione dei dati: {e}")
        return pd.DataFrame()
        
def analyze_log_with_ai(log_data):
    """Invia il log all'AI per un'analisi dettagliata."""
    if not api_key or api_key == "tuo_codice_segreto_qui":
        print("⚠️ Nota: API Key non trovata nel file .env. Eseguo simulazione (Mock).")
        return analyze_log_with_ai_MOCK(log_data) # Chiama la funzione mock
        
        
    # Inizializziamo il modello LLM
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0) #temperature=0 per risposte più precise e meno creative

    # Creiamo il Prompt (RAG logic)
    prompt = ChatPromptTemplate.from_template("""
        Sei un Senior Cloud Security Engineer. Analizza il seguente log di AWS CloudTrail.
        Determina se l'evento è pericoloso (es. Brute Force, accesso da IP sconosciuto, ecc.).
        
        DATI LOG:
        {log_detail}
        
        Fornisci un report strutturato con:
        1. LIVELLO PERICOLO (Basso/Medio/Alto)
        2. ANALISI TECNICA
        3. AZIONE CONSIGLIATA
        """)

    # Creiamo la catena di esecuzione
    chain = prompt | llm # Pipe operator per collegare prompt e modello

    # Trasformiamo il log in stringa e invochiamo l'AI
    response = chain.invoke({"log_detail": log_data.to_json()})
    return response.content

def analyze_log_with_ai_MOCK(log_data):
    """Versione di test che simula l'IA senza chiamare le API."""
    
    # Simuliamo il ritardo dell'IA
    import time
    print("... 🤖 L'IA sta analizzando il log ...")
    time.sleep(1)

    log_dict = log_data.to_dict() # Converte il log in dizionario
    ip = log_dict.get('sourceIPAddress') # Estrae l'IP sorgente
    user = log_dict.get('userIdentity', {}).get('userName', 'Unknown') # Estrae l'utente, se disponibile, altrimenti 'Unknown'. Metto {} per evitare errori se 'userIdentity' non è presente quindi restituisce un dizionario vuoto

    # Logica di analisi simulata
    analysis = f"⚠️ [REPORT MOCK]\n"
    analysis += f"SORGENTE: Accesso rilevato dall'IP {ip} (NON AUTORIZZATO).\n"
    analysis += f"UTENTE COLPITO: {user}\n"
    analysis += f"RACCOMANDAZIONE: Bloccare immediatamente l'IP tramite Security Group AWS."
    
    return analysis

def main():
    log_file = "mock_logs.json"
    print(f"--- Inizio Analisi Log: {log_file} ---")

    # 1. Caricamento e filtraggio dei log sospetti con Pandas
    suspicious_logs = load_and_filter_logs(log_file)

    if not suspicious_logs.empty:
        print(f"Trovati {len(suspicious_logs)} eventi sospetti. Avvio analisi AI...\n")
        
        # Step 2: Analisi AI (prendiamo il primo log sospetto come esempio)
        first_threat = suspicious_logs.iloc[0] 
        report = analyze_log_with_ai(first_threat)
        
        print("--- REPORT DI SICUREZZA GENERATO DALL'AI ---")
        print(report)
        print("--------------------------------------------")
    else:
        print("Nessuna minaccia rilevata nei log analizzati.")

if __name__ == "__main__":
    main()