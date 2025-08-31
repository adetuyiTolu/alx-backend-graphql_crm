import datetime
import os
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def log_crm_heartbeat():
    """
    Logs a heartbeat message every 5 minutes and queries the GraphQL endpoint.
    """
    now = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    log_file_path = "/tmp/crm_heartbeat_log.txt"
    
    # Log initial heartbeat
    log_message = f"{now} CRM is alive\n"
    with open(log_file_path, "a") as f:
        f.write(log_message)
    
    # Configure GraphQL client
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=True,
        retries=3,
    )
    client = Client(transport=transport, fetch_schema_from_transport=True)
    
    # Query hello field
    try:
        query = gql("{ hello }")
        result = client.execute(query)
        with open(log_file_path, "a") as f:
            f.write(f"{now} GraphQL hello response: {result}\n")
    except Exception as e:
        with open(log_file_path, "a") as f:
            f.write(f"{now} GraphQL check error: {str(e)}\n")
