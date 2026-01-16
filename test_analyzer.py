import pandas as pd
import pytest
from analyzer import load_and_filter_logs, AUTHORIZED_IPS

def test_filter_failed_login(tmp_path):
    """Verifica che un login fallito venga rilevato anche se l'IP è autorizzato."""
    # Creiamo un file JSON temporaneo per il test
    d = tmp_path / "test_logs.json" # Crea cartella temporanea e il file JSON
    data = [{
        "sourceIPAddress": AUTHORIZED_IPS[0], # IP sicuro
        "responseElements": {"ConsoleLogin": "Failure"}, # Ma login fallito per credenziali errate
        "userIdentity": {"userName": "test_user"}
    }]
    d.write_text(pd.Series(data).to_json(orient='records')) # Scrivi il file JSON 

    result = load_and_filter_logs(str(d))
    assert len(result) == 1 # Verifica che sia stato rilevato un log
    assert result.iloc[0]['responseElements']['ConsoleLogin'] == "Failure" # Verifica che sia stato rilevato un login fallito

def test_filter_unauthorized_ip(tmp_path):
    """Verifica che un IP non autorizzato venga rilevato anche se il login ha successo."""
    d = tmp_path / "test_logs_ip.json"
    data = [{
        "sourceIPAddress": "99.99.99.99", # IP Sconosciuto
        "responseElements": {"ConsoleLogin": "Success"}, # Login OK
        "userIdentity": {"userName": "hacker"}
    }]
    d.write_text(pd.Series(data).to_json(orient='records'))

    result = load_and_filter_logs(str(d))
    assert len(result) == 1
    assert result.iloc[0]['sourceIPAddress'] == "99.99.99.99"

def test_no_suspicious_logs(tmp_path):
    """Verifica che un log pulito non venga segnalato."""
    d = tmp_path / "test_logs_clean.json"
    data = [{
        "sourceIPAddress": AUTHORIZED_IPS[0],
        "responseElements": {"ConsoleLogin": "Success"},
        "userIdentity": {"userName": "clean_user"}
    }]
    d.write_text(pd.Series(data).to_json(orient='records'))

    result = load_and_filter_logs(str(d))
    assert len(result) == 0