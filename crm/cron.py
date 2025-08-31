import datetime
import requests
import os

def log_crm_heartbeat():
    """
    Logs a heartbeat message every 5 minutes to confirm CRM health.
    Optionally queries GraphQL hello endpoint.
    """
    # Timestamp
    now = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    
    # Log message
    log_message = f"{now} CRM is alive\n"
    
    # Path to log file
    log_file_path = "/tmp/crm_heartbeat_log.txt"
    
    # Append message to log file
    with open(log_file_path, "a") as f:
        f.write(log_message)
    
    # Optional: check GraphQL endpoint
    try:
        url = "http://localhost:8000/graphql"
        query = {"query": "{ hello }"}  # assuming your schema has a hello field
        response = requests.post(url, json=query)
        if response.status_code == 200:
            with open(log_file_path, "a") as f:
                f.write(f"{now} GraphQL hello response: {response.json()}\n")
        else:
            with open(log_file_path, "a") as f:
                f.write(f"{now} GraphQL hello failed: {response.status_code}\n")
    except Exception as e:
        with open(log_file_path, "a") as f:
            f.write(f"{now} GraphQL check error: {str(e)}\n")
