import json
import random
from datetime import datetime, timezone, timedelta
import uuid

# Configurazione utenti, eventi e IP fittizi
USERS = ["admin_alice", "dev_bob", "intern_charlie"]
EVENTS = [
    {"name": "ConsoleLogin", "source": "signin.amazonaws.com"},
    {"name": "PutObject", "source": "s3.amazonaws.com"},
    {"name": "TerminateInstances", "source": "ec2.amazonaws.com"},
    {"name": "AuthorizeSecurityGroupIngress", "source": "ec2.amazonaws.com"}
]
IPS = ["192.168.1.10", "10.0.0.50", "172.16.0.5"]

def generate_mock_log(is_suspicious=False): 
    event = random.choice(EVENTS)
    user = random.choice(USERS)
    ip = random.choice(IPS)
    status = "Success"

    if is_suspicious:
        event = {"name": "ConsoleLogin", "source": "signin.amazonaws.com"}
        ip = "185.156.175.42"
        status = "Failure"
        user = "admin_alice"
  
    base_time = datetime.now(timezone.utc) - timedelta(minutes=random.randint(0, 1000))
    
    log_entry = {
        "eventID": str(uuid.uuid4()),
        "eventTime": base_time.isoformat(timespec='seconds').replace("+00:00", "Z"), #Z indica UTC
        "eventSource": event["source"],
        "eventName": event["name"],
        "userIdentity": {"type": "IAMUser", "userName": user},
        "sourceIPAddress": ip,
        "responseElements": {"ConsoleLogin": status} if event["name"] == "ConsoleLogin" else None,
        "userAgent": "Mozilla/5.0 (AWS Management Console)"
    }
    return log_entry

def main():
    logs = [generate_mock_log(is_suspicious=False) for _ in range(19)]
    logs.append(generate_mock_log(is_suspicious=True))
    random.shuffle(logs) # Mischia i log per non avere lo sospetto sempre alla fine

    with open("mock_logs.json", "w") as f:
        json.dump(logs, f, indent=4) # Salva i log in un file JSON con indentazione per leggibilità
    
    print(f"Generati {len(logs)} log aggiornati in 'mock_logs.json'")

if __name__ == "__main__":
    main()