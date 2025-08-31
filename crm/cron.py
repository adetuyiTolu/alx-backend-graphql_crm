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


def update_low_stock():
    """
    Cron job to update low-stock products via GraphQL and log results.
    Runs every 12 hours.
    """
    now = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    log_file_path = "/tmp/low_stock_updates_log.txt"

    # Configure GraphQL client
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=True,
        retries=3,
    )
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # Define mutation
    mutation = gql("""
        mutation {
            updateLowStockProducts {
                updatedProducts {
                    name
                    stock
                }
                message
            }
        }
    """)

    try:
        result = client.execute(mutation)
        updated_products = result["updateLowStockProducts"]["updatedProducts"]
        message = result["updateLowStockProducts"]["message"]

        # Log updated products
        with open(log_file_path, "a") as f:
            f.write(f"{now} - {message}\n")
            for p in updated_products:
                f.write(f"    {p['name']}: {p['stock']}\n")
    except Exception as e:
        with open(log_file_path, "a") as f:
            f.write(f"{now} - ERROR updating low stock: {str(e)}\n")